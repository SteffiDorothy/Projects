# app.py
import streamlit as st
import pandas as pd
import os
import time
import logging
import logging.handlers
from pandera.errors import SchemaError
from src import config, synthetic_data_model, privacy_utils, evaluator, utils,validation
from src.hyperparameter_tuning import HyperparameterTuning
from src.file_check import FileCheck

# --- Configure Logging ---
# Configure logging for the Streamlit app
log_file_path_app = os.path.join(config.OUTPUT_FOLDER, 'app_streamlit.log') # Separate log file
log_level_app = logging.INFO

log_formatter_app = logging.Formatter('%(asctime)s - Streamlit - %(name)s - %(levelname)s - %(message)s')

# Get root logger
root_logger_app = logging.getLogger()
root_logger_app.setLevel(log_level_app)

# Streamlit might handle console logging, but we ensure file logging
try:
    file_handler_app = logging.FileHandler(log_file_path_app, mode='a')
    file_handler_app.setFormatter(log_formatter_app)
    # Avoid adding duplicate file handlers
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == log_file_path_app for h in root_logger_app.handlers):
        root_logger_app.addHandler(file_handler_app)
except Exception as e:
    st.warning(f"Could not configure file logging: {e}") # Show warning in UI

# Get logger for the app module itself
logger = logging.getLogger(__name__) # Keep using logger instance throughout app.py


# --- Page Configuration ---
st.set_page_config(
    page_title="AI Data Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initial Default State ---
# Define defaults here for easier reset
INITIAL_STATE = {
    'real_data': None,
    'metadata_generated': False,
    'metadata_path': None,
    'model_type': 'TVAE',
    'num_rows': 1000,
    'model_trained': False,
    'model_path': None,
    'synthetic_data_raw': None,
    'columns_to_hash': [],
    'columns_to_dp': [],
    'epsilon': 1.0,
    'privacy_method': 'hashing',  # 'hashing' or 'differential'
    'synthetic_data_processed': None,
    'evaluation_done': False,
    'eval_instance': None,
    'original_file_path': None,
    'original_filename': "data",
    'temp_dir': "temp_data", # Keep temp_dir definition consistent
    'process_running': False,
    'custom_metrics_results': {},
    'custom_metrics_summary': {},
    'enable_tuning': False
}

# --- Initialize Session State ---
def init_session_state():
    """Initializes session state with default values."""
    # Ensure temp_dir exists even if state cleared
    st.session_state.setdefault('temp_dir', "temp_data")
    for key, value in INITIAL_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize on first run
init_session_state()

# --- Helper Functions ---
def reset_workflow(clear_data=False):
    """Resets the state for subsequent steps or completely."""
    logging.info(f"Resetting workflow state (clear_data={clear_data})")

    if clear_data:
        # --- START: File Deletion Logic ---
        # (Keep this part the same as before)
        try:
            if st.session_state.get('original_filename') and st.session_state.get('model_type'):
                logging.info("Attempting to delete previous output files...")
                prev_meta_file = os.path.join(config.OUTPUT_FOLDER, f"{st.session_state['original_filename']}_metadata.json")
                prev_model_file = os.path.join(config.MODELS_FOLDER, f"{st.session_state['original_filename']}_{st.session_state['model_type']}.pkl")
                prev_synth_file = os.path.join(config.OUTPUT_FOLDER, f"synthetic_{st.session_state['original_filename']}.csv")

                for f_path in [prev_meta_file, prev_model_file, prev_synth_file]:
                    if os.path.exists(f_path):
                        try:
                            os.remove(f_path)
                            logging.info(f"Deleted previous file: {f_path}")
                        except OSError as e:
                            logging.warning(f"Could not delete previous file {f_path}: {e}")
        except Exception as e:
             logging.error(f"Error during path construction or deletion in reset: {e}")
        # --- END: File Deletion Logic ---

        # Iterate over a copy of keys and delete all state defined in INITIAL_STATE
        keys_to_delete = list(st.session_state.keys()) # Get current keys
        logging.info(f"Attempting to clear state keys: {keys_to_delete}")
        for key in keys_to_delete:
            # Optionally keep certain persistent keys if needed, but for full reset, delete all known keys
            if key in INITIAL_STATE: # Only delete keys we defined as part of the workflow state
                try:
                    del st.session_state[key]
                except KeyError:
                    pass # Key might have already been deleted if code runs unexpectedly fast
        logging.info("Session state keys cleared.")
        # Re-initialize state to defaults
        init_session_state()
        logging.info("Session state re-initialized to defaults.")


        # Cleanup temp directory
        # (Keep this part the same as before)
        if os.path.exists(st.session_state['temp_dir']):
             try:
                 for f in os.listdir(st.session_state['temp_dir']):
                     f_path = os.path.join(st.session_state['temp_dir'], f)
                     if os.path.isfile(f_path): os.remove(f_path)
                 logging.info(f"Cleaned temp directory: {st.session_state['temp_dir']}")
             except Exception as e:
                 logging.warning(f"Could not fully clean temp directory: {e}")

    else: # Partial reset logic remains the same (for steps other than Upload New File)
        st.session_state['metadata_generated'] = False
        st.session_state['metadata_path'] = None
        st.session_state['model_trained'] = False
        st.session_state['model_path'] = None
        st.session_state['synthetic_data_raw'] = None
        st.session_state['synthetic_data_processed'] = None
        st.session_state['evaluation_done'] = False
        st.session_state['eval_instance'] = None
        st.session_state['custom_metrics_results'] = {}
        st.session_state['custom_metrics_summary'] = {}


try:
    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(config.MODELS_FOLDER, exist_ok=True)
    os.makedirs(config.PLOTS_FOLDER, exist_ok=True)
    os.makedirs(config.METRICS_PATH, exist_ok=True)
    os.makedirs(st.session_state.get('temp_dir', "temp_data"), exist_ok=True)
except OSError as e:
     st.error(f"Failed to create necessary directories: {e}.")
     logger.error(f"Directory creation failed: {e}")
# ==================================
# Sidebar: Configuration & Actions
# ==================================
with st.sidebar:
    st.header("⚙️ Model Configuration")

    st.selectbox(
        "Select Synthesizer Model", ('TVAE', 'CTGAN', 'GaussianCopula'), key='model_type', index=0,
        help="Choose the algorithm for synthetic data generation.",
        disabled=st.session_state['process_running']
    )

    # Add hyperparameter tuning options
    if st.checkbox("Enable Hyperparameter Tuning", key='enable_tuning'):
        HyperparameterTuning.display_tuning_options(st.session_state['model_type'])

    st.number_input(
        "Number of Synthetic Samples", min_value=10, step=100, key='num_rows',
        help="How many rows of synthetic data to generate.",
        disabled=st.session_state['process_running']
    )

    st.divider(); st.header("🚀 Actions")

    # --- Action Buttons ---
    # 1. Generate Metadata
    metadata_btn_disabled = (
        st.session_state['process_running'] or
        st.session_state.get('real_data') is None or
        st.session_state.get('metadata_generated', False)
    )
    # Check if real_data exists in session state before showing button logic
    if st.session_state.get('real_data') is not None:
        if st.button("1. Generate Metadata", disabled=metadata_btn_disabled, key='btn_meta'):
            # progress = st.progress(0) # Progress bar might be too fast here
            st.session_state['process_running'] = True
            reset_workflow(clear_data=False) # Call partial reset for subsequent steps

            # Define metadata path using original filename from state
            meta_path = os.path.join(config.OUTPUT_FOLDER, f"{st.session_state.get('original_filename', 'metadata')}_metadata.json")

            try:
                with st.spinner("Detecting metadata..."):
                    # --- CORRECTED LOGIC ---
                    # Check if real_data DataFrame actually exists in state
                    if st.session_state.get('real_data') is not None and not st.session_state['real_data'].empty:
                        # Import Metadata class (can be done locally or at top)
                        from sdv.metadata import Metadata
                        logger.info("Detecting metadata directly from real_data dataframe in session state...")

                        # Detect metadata directly from the loaded DataFrame
                        detected_metadata = Metadata.detect_from_dataframe(data=st.session_state['real_data'])

                        # Ensure output directory exists before saving
                        output_dir = os.path.dirname(meta_path)
                        if output_dir:
                            os.makedirs(output_dir, exist_ok=True)

                        # Save the detected metadata
                        detected_metadata.save_to_json(filepath=meta_path)
                        logger.info(f"Metadata saved to {meta_path}")
                        # --- END CORRECTED LOGIC ---

                        st.session_state['metadata_path'] = meta_path
                        st.session_state['metadata_generated'] = True
                        st.success(f"Metadata generated: {meta_path}")
                    else:
                        # This case should ideally not be reached if button is correctly disabled
                        st.error("Real data not found in session state for metadata detection.")
                        logger.error("Real data missing during metadata generation step.")

            except Exception as e:
                st.error(f"Metadata generation failed: {e}"); logging.error("Metadata generation failed", exc_info=True)

            st.session_state['process_running'] = False
            st.rerun() # Rerun to update UI state based on metadata_generated flag


    # 2. Train Model
    train_btn_disabled = st.session_state['process_running'] or not st.session_state.get('metadata_generated', False) or st.session_state.get('model_trained', False)
    if st.session_state.get('metadata_generated'):
        if st.button("2. Train Synthesizer", disabled=train_btn_disabled, key='btn_train'):
            progress = st.progress(0)
            st.session_state['process_running'] = True
            st.session_state['model_trained'] = False
            st.session_state['model_path'] = None
            st.session_state['synthetic_data_raw'] = None
            st.session_state['synthetic_data_processed'] = None
            st.session_state['evaluation_done'] = False
            try:
                model_file = f"{st.session_state['original_filename']}_{st.session_state['model_type']}.pkl"
                m_path = os.path.join(config.MODELS_FOLDER, model_file)
                if os.path.exists(m_path):
                    try:
                        os.remove(m_path)
                        logging.info(f"Removed existing model: {m_path}")
                    except OSError as e_rm:
                        logging.warning(f"Could not remove model {m_path}: {e_rm}")

                with st.spinner(f"Training {st.session_state['model_type']}..."):
                    if st.session_state['real_data'] is not None:
                        # Get tuned parameters if enabled
                        model_params_to_pass = {} # Start with empty dict
                        if st.session_state.get('enable_tuning', False):
                            # If tuning is enabled, get the user's selections
                            logger.info("Hyperparameter tuning enabled. Getting tuned parameters from UI.")
                            model_params_to_pass = HyperparameterTuning.get_tuned_params(st.session_state['model_type'])
                        else:
                            # If tuning is disabled, pass an empty dict.
                            # The create_model function will now fetch defaults from config internally.
                            logger.info("Hyperparameter tuning disabled. Using defaults defined in config.")
                            # No need to explicitly pass defaults here anymore.
                            # model_params_to_pass = {} # Already initialized above

                        logger.debug(f"Parameters being passed to create_model: {model_params_to_pass}")

                        # Call create_model, unpacking the determined parameters
                        synthetic_data_model.SyntheticDataModel.create_model(
                            st.session_state['real_data'],
                            st.session_state['metadata_path'],
                            m_path,
                            st.session_state['model_type'],
                            **model_params_to_pass # Unpack the dictionary
                        )


                        st.session_state['model_path'] = m_path
                        st.session_state['model_trained'] = True
                        st.success(f"Model trained: {m_path}")

                    else:
                        st.error("Real data not found.")

            except Exception as e:
                st.error(f"Training failed: {e}")
                logging.error("Training failed", exc_info=True)
            st.session_state['process_running'] = False
            st.rerun()

    # 3. Generate Synthetic Data
    gen_btn_disabled = st.session_state['process_running'] or not st.session_state.get('model_trained', False) or st.session_state.get('synthetic_data_raw') is not None
    if st.session_state.get('model_trained'):
         if st.button("3. Generate Data", disabled=gen_btn_disabled, key='btn_gen'):
            progress = st.progress(0)
            st.session_state['process_running'] = True
            st.session_state['synthetic_data_raw'] = None; st.session_state['synthetic_data_processed'] = None
            st.session_state['evaluation_done'] = False
            try:
                with st.spinner(f"Generating {st.session_state['num_rows']} samples..."):
                     if st.session_state.get('model_path') and os.path.exists(st.session_state['model_path']):
                         synth_data = synthetic_data_model.SyntheticDataModel.generate_synthetic_data(st.session_state['num_rows'])
                         st.session_state['synthetic_data_raw'] = synth_data
                         st.session_state['synthetic_data_processed'] = synth_data # Set processed = raw initially
                         st.success(f"Generated {len(synth_data)} rows.")
                     else: st.error("Trained model path not found.")
            except Exception as e: st.error(f"Generation failed: {e}"); logging.error("Generation failed", exc_info=True)
            st.session_state['process_running'] = False
            st.rerun()

    # 4. Apply Privacy Protection (Optional)
    if st.session_state.get('synthetic_data_raw') is not None:
        st.divider(); st.subheader("4. Apply Privacy Protection")
        
        # Privacy Method Selection
        privacy_method = st.radio(
            "Select Privacy Protection Method:",
            ["Hashing", "Differential Privacy"],
            key='privacy_method',
            help="Choose between hashing sensitive columns or applying differential privacy"
        )
        
        available_columns = st.session_state['synthetic_data_raw'].columns.tolist()
        
        if privacy_method == "Hashing":
            # Hashing options
            st.multiselect(
                "Select columns to hash:",
                options=available_columns,
                key='columns_to_hash',
                help="Select columns containing sensitive information to hash"
            )

            if st.button("Apply Hashing", disabled=st.session_state['process_running'], key='btn_hash'):
                st.session_state['process_running'] = True
                st.session_state['evaluation_done'] = False
                st.session_state['eval_instance'] = None

                if st.session_state['columns_to_hash']:
                    try:
                        with st.spinner("Applying hashing..."):

                            # Instantiate PrivacyUtils
                            privacy_handler = privacy_utils.PrivacyUtils()
                            # Call method on the instance
                            hashed_data = privacy_handler.apply_hashing(
                                st.session_state['synthetic_data_raw'],
                                st.session_state['columns_to_hash']
                            )

                            st.session_state['synthetic_data_processed'] = hashed_data
                        st.success(f"Hashing applied to: {st.session_state['columns_to_hash']}")
                    except Exception as e:
                        st.error(f"Hashing failed: {e}")
                        logging.error("Hashing failed", exc_info=True)
                else:
                    st.info("No columns selected. Using unhashed generated data.")
                    st.session_state['synthetic_data_processed'] = st.session_state['synthetic_data_raw']

                st.session_state['process_running'] = False
                st.rerun()

        else:  # Differential Privacy
            # DP options
            st.multiselect(
                "Select columns for differential privacy:",
                options=[col for col in available_columns if
                         pd.api.types.is_numeric_dtype(st.session_state['synthetic_data_raw'][col])],
                # Only show numeric cols
                key='columns_to_dp',
                help="Select NUMERIC columns to apply differential privacy protection"
            )

            st.slider(
                "Privacy Budget (ε):",
                min_value=0.1,
                max_value=10.0,  # Increased max for flexibility
                value=1.0,
                step=0.1,
                key='epsilon',
                help="Lower values provide stronger privacy but may reduce data utility (Must be > 0)"
            )

            if st.button("Apply Differential Privacy", disabled=st.session_state['process_running'], key='btn_dp'):
                st.session_state['process_running'] = True
                st.session_state['evaluation_done'] = False
                st.session_state['eval_instance'] = None

                if st.session_state['columns_to_dp']:
                    try:
                        with st.spinner("Applying differential privacy..."):
                            # Use the merged function from PrivacyUtils
                            privacy_handler = privacy_utils.PrivacyUtils()

                            dp_data = privacy_handler.add_laplace_noise(
                                st.session_state['synthetic_data_raw'],
                                st.session_state['columns_to_dp'],
                                st.session_state['epsilon']

                            )
                            st.session_state['synthetic_data_processed'] = dp_data
                            st.success(f"Differential privacy applied to: {st.session_state['columns_to_dp']}")
                    except Exception as e:
                        st.error(f"Differential privacy application failed: {e}")
                        logging.error("DP application failed", exc_info=True)
                else:
                    st.info("No columns selected for differential privacy. Using original generated data.")
                    # Ensure processed data reflects the raw if nothing was done
                    st.session_state['synthetic_data_processed'] = st.session_state['synthetic_data_raw']

                st.session_state['process_running'] = False
                st.rerun()

        st.divider()

    # 5. Evaluate Data
    eval_button_disabled = st.session_state['process_running'] or st.session_state.get('synthetic_data_processed') is None or st.session_state.get('evaluation_done', False)
    if st.session_state.get('synthetic_data_processed') is not None:
        if st.button("5. Evaluate Synthetic Data", disabled=eval_button_disabled, key='btn_eval'):
            st.session_state['process_running'] = True
            st.session_state['evaluation_done'] = False # Reset only eval state
            try:
                with st.spinner("Evaluating data quality..."):
                    if st.session_state.get('real_data') is not None and st.session_state.get('synthetic_data_processed') is not None:
                        eval_instance = evaluator.EvaluateSynthetic(st.session_state['real_data'], st.session_state['synthetic_data_processed'], st.session_state.get('metadata_path'))
                        st.session_state['eval_instance'] = eval_instance
                        st.session_state['custom_metrics_results'] = eval_instance.evaluate_all_columns_custom()
                        st.session_state['custom_metrics_summary'] = eval_instance.get_custom_metrics_summary(st.session_state['custom_metrics_results'])
                        st.session_state['evaluation_done'] = True
                        st.success("Evaluation complete.")
                    else: st.warning("Input data missing for evaluation.")
            except Exception as e: st.error(f"Evaluation failed: {e}", icon="🚨"); logging.error("Evaluation failed", exc_info=True)
            st.session_state['process_running'] = False
            st.rerun()

    # --- Sidebar Footer/Status ---
    st.sidebar.divider()
    if st.session_state.get('process_running'): st.sidebar.warning("⏳ Process running...")
    elif st.session_state.get('real_data') is None: st.sidebar.info("Status: Waiting for data upload.")
    else: # Status messages based on progress
        if not st.session_state.get('metadata_generated'): status_msg = "Status: Ready for Metadata Generation."
        elif not st.session_state.get('model_trained'): status_msg = "Status: Ready for Model Training."
        elif st.session_state.get('synthetic_data_raw') is None: status_msg = "Status: Ready for Data Generation."
        elif not st.session_state.get('evaluation_done'): status_msg = "Status: Ready for Evaluation."
        else: status_msg = "Status: Evaluation Complete."
        st.sidebar.info(status_msg)



# ==================================
# Main Area: Upload & Results
# ==================================

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>EOTSS AI Data Generator</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: grey;'>Gen AI-Powered Data Generator</h3>", unsafe_allow_html=True)
st.divider()

# --- File Upload & Reset ---
if st.session_state.get('real_data') is None:
    uploaded_file = st.file_uploader(
        "Drag and drop CSV, JSON, XLSX, or XLS here",
        type=['csv', 'json', 'xlsx', 'xls'],  # Accept new types
        key='main_uploader'
    )
    if uploaded_file:
        st.session_state['process_running'] = True
        with st.spinner("Loading and processing data..."):
            temp_path = os.path.join(st.session_state['temp_dir'], uploaded_file.name)
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            try:
                # Save uploaded file temporarily
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.session_state['original_file_path'] = temp_path
                st.session_state['original_filename'] = os.path.splitext(uploaded_file.name)[0]
                logger.info(f"File uploaded to temp path: {temp_path}")

                # --- CSV Specific Preprocessing ---
                if file_extension == '.csv':
                    file_checker = FileCheck()  # Instantiate FileCheck only for CSV
                    logger.info(f"Checking/Converting delimiter for CSV file: {temp_path}")
                    if not file_checker.convert_to_comma_delimited(temp_path):
                        raise ValueError(f"Could not process CSV file delimiter for {uploaded_file.name}.")
                    logger.info(f"CSV file ensured to be comma-delimited: {temp_path}")
                # --- End CSV Specific ---

                # --- Load data based on extension ---
                df_loaded = None
                logger.info(f"Loading data from {file_extension} file: {temp_path}")
                if file_extension == '.csv':
                    df_loaded = utils.load_csv(temp_path)
                elif file_extension == '.json':
                    # Provide guidance or common defaults
                    st.info(
                        "Loading JSON assuming 'records' orientation. Adjust code if needed for different JSON structures.")
                    df_loaded = utils.load_json(temp_path, orient='records')
                elif file_extension in ['.xlsx', '.xls']:
                    st.info("Loading first sheet from Excel file.")
                    df_loaded = utils.load_excel(temp_path, sheet_name=0)
                else:
                    raise ValueError(f"Unsupported file type uploaded: {file_extension}")

                if df_loaded is None:  # Check if loading function failed
                    raise ValueError(f"Failed to load data from file {uploaded_file.name}.")
                logger.info(f"Data loaded from {temp_path}, shape: {df_loaded.shape}")
                # --- End Loading ---

                # --- Validation Step (remains the same) ---
                logger.info("Performing input data validation...")
                st.info("Validating uploaded data...")  # User feedback
                df_validated = validation.validate_data(df_loaded)
                logger.info("Input data validation successful.")
                st.success("Data validation passed.")
                # --- END VALIDATION STEP ---

                # Preprocess (fillna) AFTER validation
                logger.info("Applying forward fill...")
                df_processed = df_validated.fillna(method='ffill')

                st.session_state['real_data'] = df_processed
                logger.info(f"State after upload: real_data is set (shape {st.session_state['real_data'].shape})")
                time.sleep(1)

            except (SchemaError, ValueError) as ve:
                st.error(f"Data Processing Failed: {ve}")
                logger.error(f"Input data processing failed: {ve}", exc_info=True)
                reset_workflow(clear_data=True)

            except Exception as e:
                st.error(f"Failed to read/process file: {e}")
                logger.error(f"Upload/Processing failed", exc_info=True)
                reset_workflow(clear_data=True)

            finally:
                st.session_state['process_running'] = False
                st.rerun()

else:  # This block runs if real_data IS loaded
    # Display original filename (add extension back for clarity)
    display_filename = f"{st.session_state['original_filename']}{os.path.splitext(st.session_state['original_file_path'])[1]}" if st.session_state.get('original_file_path') else "uploaded file"
    st.info(f"Using uploaded file: **{display_filename}**")
    if st.button("Upload New File", key="clear_data_button", disabled=st.session_state['process_running']):
        reset_workflow(clear_data=True)
        st.rerun()


# --- Data Previews ---
if st.session_state.get('real_data') is not None:
    with st.expander("📊 Preview of Uploaded Data", expanded=st.session_state.get('synthetic_data_processed') is None):
        st.dataframe(st.session_state['real_data'].head())

if st.session_state.get('synthetic_data_processed') is not None:
    with st.expander("✨ Preview of Generated Synthetic Data", expanded=True):
        st.dataframe(st.session_state['synthetic_data_processed'].head())
        try: # Download button logic
            processed_data_csv = st.session_state['synthetic_data_processed'].to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Synthetic Data (CSV)", data=processed_data_csv,
                               file_name=f"synthetic_{st.session_state['original_filename']}.csv",
                               mime='text/csv', key='download_synth_csv')
        except Exception as e: st.error(f"Failed to prepare download: {e}")


# --- Evaluation Results ---
# --- Evaluation Results ---
if st.session_state.get('evaluation_done'):
    st.divider()
    st.header("📈 Evaluation Results")
    eval_instance = st.session_state.get('eval_instance')

    if eval_instance:
        # Metrics Summary
        with st.container(border=True):
            st.subheader("Custom Metric Summary")
            summary = st.session_state.get('custom_metrics_summary', {})
            ws_summary = summary.get('wasserstein', {})
            kl_summary = summary.get('kl_divergence', {})
            col1, col2 = st.columns(2)
            ws_mean = ws_summary.get('mean')
            kl_mean = kl_summary.get('mean')
            with col1:
                st.metric(label="Avg. Wasserstein Distance", value=f"{ws_mean:.4f}" if ws_mean is not None else "N/A")
            with col2:
                st.metric(label="Avg. KL Divergence", value=f"{kl_mean:.4f}" if kl_mean is not None else "N/A")

            with st.expander("Detailed Custom Metrics"):
                try:
                    detailed_metrics_df = pd.DataFrame.from_dict(
                        st.session_state.get('custom_metrics_results', {}), orient='index'
                    )
                    st.dataframe(detailed_metrics_df.style.format(precision=4, na_rep='N/A'))
                    detailed_metrics_csv = detailed_metrics_df.to_csv().encode('utf-8')
                    st.download_button(
                        label="Download Detailed Metrics (CSV)",
                        data=detailed_metrics_csv,
                        file_name=f"detailed_metrics_{st.session_state['original_filename']}.csv",
                        mime='text/csv',
                        key='download_metrics_csv'
                    )
                except Exception as e:
                    st.error(f"Failed to display/prepare detailed metrics: {e}")

        # Correlation Comparison
        st.subheader("Correlation Comparison")
        try:
            # Get the eval_instance from session state
            eval_instance = st.session_state.get('eval_instance')
            if eval_instance:
                # Add dropdown to select correlation method
                corr_method = st.selectbox(
                    "Select Correlation Method:",
                    ('pearson', 'spearman', 'kendall'),
                    key='corr_method_select'
                )

                corr_fig = eval_instance.create_correlation_heatmap(method=corr_method)
                if corr_fig:
                    st.plotly_chart(corr_fig, use_container_width=True)
                else:
                    st.info("Not enough numeric columns (minimum 2 required) to generate correlation heatmap.")
            else:
                st.warning("Evaluation instance not found, cannot generate correlation heatmap.")
        except Exception as e:
            st.error(f"Failed to generate or display correlation heatmap: {e}")
            logger.error("Correlation heatmap failed in app.py", exc_info=True)

        # Distribution Comparison Plots
        st.subheader("Distribution Comparison Plots")
        plot_errors = 0
        plot_success = 0
        num_cols = 3

        if hasattr(eval_instance, 'common_columns') and eval_instance.common_columns:
            with st.spinner("Generating plots..."):
                plot_area = st.container()
                plot_cols = plot_area.columns(num_cols)
                col_idx = 0

                for column in sorted(eval_instance.common_columns):
                    try:
                        fig = eval_instance.create_distribution_plot(column)
                        if fig and hasattr(fig, 'data') and len(fig.data) > 0:
                            with plot_cols[col_idx % num_cols]:
                                st.plotly_chart(fig, use_container_width=True)
                            plot_success += 1
                            col_idx += 1
                        else:
                            logging.warning(f"Plot generation for '{column}' returned empty or invalid figure.")
                            plot_errors += 1
                    except Exception as e:
                        logging.error(f"Error during plot generation for '{column}': {e}", exc_info=True)
                        with plot_cols[col_idx % num_cols]:
                            st.error(f"Plot Error ({column})", icon="⚠️")
                        plot_errors += 1
                        col_idx += 1

                st.caption(f"Successfully generated {plot_success} plots. Encountered {plot_errors} errors/skips.")
        else:
            st.warning("Cannot generate plots: Common columns missing.")
