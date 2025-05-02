# src/Main.py
import pandas as pd
from sdv.single_table import GaussianCopulaSynthesizer, CTGANSynthesizer, TVAESynthesizer
import metadata_converter
import synthetic_data_model # Keep import for generate_data
import evaluator
import file_check
import config
import os
import utils
from file_check import FileCheck
from privacy_utils import PrivacyUtils
from metadata_converter import MetadataConverter
import cli_handler
import validation
import logging
import logging.handlers
import sys
from pandera.errors import SchemaError

# --- Logging Configuration (keep as previously updated) ---
log_file_path = os.path.join(config.OUTPUT_FOLDER, 'app_main.log')
log_level = logging.INFO
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
root_logger = logging.getLogger()
root_logger.setLevel(log_level)
# Console Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
    root_logger.addHandler(console_handler)
# File Handler
try:
    file_handler = logging.FileHandler(log_file_path, mode='a')
    file_handler.setFormatter(log_formatter)
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == log_file_path for h in root_logger.handlers):
         root_logger.addHandler(file_handler)
except Exception as e:
    print(f"Warning: Could not configure file logging to {log_file_path}: {e}")
logger = logging.getLogger(__name__)
# --- End Logging Configuration ---


def main():
    logger.info("Starting Main script execution.")

    file_checker = FileCheck()
    privacy_handler = PrivacyUtils()
    metadata_handler = MetadataConverter()

    # --- Path Setup (keep as before) ---
    D = config.DATA_FOLDER
    output_folder = config.OUTPUT_FOLDER
    models_folder = config.MODELS_FOLDER
    metadata_path = config.METADATA_PATH
    plots_folder = os.path.join(output_folder, config.PLOTS)
    metrics_path = os.path.join(output_folder, config.METRICS)

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(models_folder, exist_ok=True)
    os.makedirs(plots_folder, exist_ok=True)
    os.makedirs(metrics_path, exist_ok=True)

    # --- File Discovery and Preprocessing (keep as before) ---
    file_path = file_checker.get_latest_data_file(D)  # <--- UPDATED CALL
    if not file_path:
        logger.error(f"No supported data files (.csv, .json, .xlsx, .xls) found in '{D}'.")  # Updated message
        print(f"No supported data files found in '{D}'. Please add a file and try again.")
        return
    logger.info(f"Using data file: {file_path}")
    print(f"Using data file: {file_path}")

    # --- File Type Specific Preprocessing (Delimiter Check for CSV) ---
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.csv':  # Only perform delimiter check for CSV files
        logger.info("Step 1: Checking and Converting CSV File")
        print("\n--- Checking and Converting CSV File ---")
        try:
            if not file_checker.convert_to_comma_delimited(file_path):
                logger.error(f"Failed to ensure CSV file is comma-delimited: {file_path}")
                print(f"ERROR: Failed to process CSV file delimiter for {file_path}")
                return
        except Exception as e:
            logger.error(f"Error during CSV conversion check: {e}", exc_info=True)
            print(f"ERROR: Failed during CSV file processing: {e}")
            return
    else:
        logger.info(f"Skipping delimiter check for non-CSV file type: {file_extension}")

    # --- Load, Validate, Preprocess Data (keep as before) ---
    logger.info("Step 2: Loading and Preprocessing Real Data")
    print("\n--- Loading and Preprocessing Real Data ---")
    real_data = None # Initialize
    try:

        logger.info(f"Loading data from {file_extension} file: {file_path}")
        if file_extension == '.csv':
            real_data = utils.load_csv(file_path)
        elif file_extension == '.json':
            # May need specific orient/lines based on JSON structure
            # Example: common case is records per line
            real_data = utils.load_json(file_path, orient='records', lines=False) # Adjust as needed
            if real_data is None: # Check if load_json itself failed
                 raise ValueError("Failed to load JSON, check format/orient/lines.")
        elif file_extension in ['.xlsx', '.xls']:
            # Load the first sheet by default
            real_data = utils.load_excel(file_path, sheet_name=0)
            if real_data is None: # Check if load_excel itself failed
                 raise ValueError("Failed to load Excel, check sheet name/library installs.")
        else:
            # Should not happen if get_latest_data_file worked correctly
            raise ValueError(f"Unsupported file type encountered: {file_extension}")


        if real_data is None: # General check if loading failed
             logger.error(f"Failed to load real data from {file_path}")
             print(f"ERROR: Could not load data file: {file_path}")
             return

        logger.info("Performing input data validation...")
        real_data = validation.validate_data(real_data)
        logger.info("Input data validation successful.")

        logger.info("Applying forward fill for missing values...")
        print("Applying forward fill for missing values...")
        real_data.fillna(method='ffill', inplace=True)
        logger.info("Real data loaded and preprocessed.")
        print("Real data loaded and preprocessed.")

    except (SchemaError, ValueError) as ve:
        logger.error(f"Data loading or validation failed: {ve}", exc_info=True) # Include stack trace for ValueErrors too
        print(f"ERROR: Data loading or validation failed: {ve}")
        return
    except Exception as e:
        logger.error(f"Error loading or preprocessing data: {e}", exc_info=True)
        print(f"ERROR: Failed to load or preprocess data: {e}")
        return


    # --- Metadata Creation ---
    logger.info("Step 3: Creating Metadata")
    print("\n--- Creating Metadata ---")
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    metadata_filename = f"{base_filename}_{config.METADATA_FILENAME}"
    metadata_path = os.path.join(output_folder, metadata_filename)
    try:
        # --- MODIFICATION START: Metadata based on loaded dataframe ---
        if real_data is not None:
            logger.info("Detecting metadata from loaded dataframe...")
            # Use the Metadata class directly
            from sdv.metadata import Metadata  # Import here or at top
            detected_metadata = Metadata.detect_from_dataframe(data=real_data)
            detected_metadata.save_to_json(filepath=metadata_path)
            logger.info(f"Metadata saved to: {metadata_path}")
            print(f"Metadata saved to: {metadata_path}")
        else:
            raise ValueError("Cannot generate metadata as real_data was not loaded.")
        # --- MODIFICATION END ---
        # Note: The instantiated metadata_handler is not strictly needed here anymore
        # if we detect directly from the loaded dataframe. Kept instantiation for consistency.

    except Exception as e:
        logger.error(f"Error creating metadata: {e}", exc_info=True)
        print(f"ERROR: Failed to create metadata: {e}")
        return

    # --- Get Model Type from User (keep as before) ---
    model_type = cli_handler.get_model_choice()
    if not model_type:
        logger.error("Model selection failed or was skipped.")
        print("Model selection failed. Exiting.")
        return

    # --- Define Model Path based on type and input file ---
    model_filename = f"{base_filename}_{model_type}_{config.MODEL_FILENAME}"
    model_path = os.path.join(models_folder, model_filename)
    logger.info(f"Model path set to: {model_path}")

    # --- Step 4: Load Existing Model OR Train New Model ---
    logger.info("Step 4: Checking for existing model or training new one.")
    load_existing = False
    if os.path.exists(model_path):
        print(f"\\n--- Found Existing Model ---")
        print(f"An existing model file was found at: {model_path}")
        while True:
            choice = input("Load existing model? (yes/no): ").strip().lower()
            if choice == 'yes':
                load_existing = True
                break
            elif choice == 'no':
                logger.info("User chose to overwrite existing model.")
                print("Proceeding to train a new model (will overwrite existing file).")
                load_existing = False
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    model_loaded_or_trained = False
    if load_existing:
        logger.info(f"Attempting to load existing {model_type} model from {model_path}")
        print(f"Loading existing {model_type} model...")
        try:
            # Load using the specific class based on model_type
            if model_type == 'GaussianCopula':
                loaded_synthesizer = GaussianCopulaSynthesizer.load(filepath=model_path)
            elif model_type == 'CTGAN':
                loaded_synthesizer = CTGANSynthesizer.load(filepath=model_path)
            elif model_type == 'TVAE':
                loaded_synthesizer = TVAESynthesizer.load(filepath=model_path)
            else:
                # This case should not be reached if model_type is validated earlier
                raise ValueError(f"Cannot load unknown model type: {model_type}")

            # Assign the loaded synthesizer to the class variable for generation
            synthetic_data_model.SyntheticDataModel.synthesizer = loaded_synthesizer
            model_loaded_or_trained = True
            logger.info(f"Successfully loaded model from {model_path}")
            print("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load existing model from {model_path}: {e}", exc_info=True)
            print(f"ERROR: Failed to load the existing model: {e}")
            print("Proceeding to train a new model instead.")
            load_existing = False # Force training if loading failed

    if not load_existing:
        logger.info(f"Training new {model_type} model.")
        print(f"\\n--- Training New {model_type} Model ---")
        try:
            # Call create_model which handles training and saving
            synthetic_data_model.SyntheticDataModel.create_model(
                data=real_data,
                metadata_path=metadata_path,
                model_path=model_path, # Pass the specific path
                model_type=model_type
                # Add **kwargs for hyperparameters here if needed later
            )
            model_loaded_or_trained = True # Training also sets the class variable
            logger.info(f"New model trained and saved to: {model_path}")
            print(f"Model trained and saved to: {model_path}")
        except Exception as e:
            logger.error(f"Error training new model: {e}", exc_info=True)
            print(f"ERROR: Failed to train model: {e}")
            return # Stop if training fails

    # Ensure model is ready before proceeding
    if not model_loaded_or_trained or synthetic_data_model.SyntheticDataModel.synthesizer is None:
         logger.critical("Model synthesizer is not available after load/train attempt. Exiting.")
         print("FATAL ERROR: Model could not be loaded or trained.")
         return

    # --- Get Number of Rows from User (keep as before) ---
    default_rows = len(real_data)
    num_rows = cli_handler.get_num_rows(default_rows)

    # --- Generate Synthetic Data (keep as before) ---
    logger.info(f"Step 5: Generating {num_rows} Synthetic Data Rows")
    print("\\n--- Generating Synthetic Data ---")
    try:
        # Now uses the loaded or newly trained synthesizer via the class variable
        synthetic_data_raw = synthetic_data_model.SyntheticDataModel.generate_synthetic_data(num_rows)
        logger.info(f"Raw synthetic data generated ({len(synthetic_data_raw)} rows).")
        print(f"Raw synthetic data generated.")
    except Exception as e:
        logger.error(f"Error generating synthetic data: {e}", exc_info=True)
        print(f"ERROR: Failed to generate synthetic data: {e}")
        return

    # --- Define Synthetic Data Path ---
    synthetic_filename = f"{base_filename}_{model_type}_synthetic_{num_rows}rows.csv"
    synthetic_data_path = os.path.join(output_folder, synthetic_filename)


    # --- Hashing ---
    pii_columns_to_hash = cli_handler.get_columns_to_hash(synthetic_data_raw.columns)
    synthetic_data_processed = synthetic_data_raw
    if pii_columns_to_hash:
        logger.info(f"Applying hashing to columns: {pii_columns_to_hash}")
        print("Applying hashing...")
        try:
            # Use the instance privacy_handler
            synthetic_data_processed = privacy_handler.apply_hashing(synthetic_data_raw,
                                                                     pii_columns_to_hash)  # <--- UPDATED CALL
            logger.info("Hashing applied successfully.")
            print("Hashing applied.")
        except Exception as e:
            logger.error(f"Error applying hashing: {e}", exc_info=True)
            print(f"WARNING: Failed to apply hashing: {e}. Continuing with unhashed data.")
            synthetic_data_processed = synthetic_data_raw

    # --- Save Synthetic Data (keep as before, but use new path) ---
    logger.info("Saving final synthetic data.")
    print(f"\\n--- Saving Synthetic Data ---")
    try:
        utils.save_csv(synthetic_data_processed, synthetic_data_path) # Use defined path
        logger.info(f"Final synthetic data saved to: {synthetic_data_path}")
        print(f"Final synthetic data saved to: {synthetic_data_path}")
    except Exception as e:
        logger.error(f"Error saving synthetic data: {e}", exc_info=True)
        print(f"ERROR: Failed to save synthetic data: {e}")


    # --- Evaluation (keep as before) ---
    logger.info("Step 6: Evaluating Synthetic Data")
    print("\\n--- Evaluating Synthetic Data ---")
    try:
        eval_instance = evaluator.EvaluateSynthetic(
            real_data=real_data,
            synthetic_data=synthetic_data_processed,
            metadata_path=metadata_path
        )
        # ... (rest of evaluation logic as before) ...
        # Calculate Custom Metrics First
        logger.info("Calculating custom metrics (Wasserstein, KL Divergence)...")
        print("Calculating custom metrics (Wasserstein, KL Divergence)...")
        custom_metrics_results = eval_instance.evaluate_all_columns_custom() # Calculate per-column
        custom_metrics_summary = eval_instance.get_custom_metrics_summary(custom_metrics_results) # Get summary

        # Save custom metrics to file
        logger.info("Saving custom metrics...")
        # Define metric paths based on output file name
        metrics_summary_file = os.path.join(metrics_path, f"{base_filename}_{model_type}_metrics_summary.txt")
        metrics_detailed_file = os.path.join(metrics_path, f"{base_filename}_{model_type}_metrics_detailed.csv")

        with open(metrics_summary_file, 'w') as f:
             f.write("Custom Metric Summary (Lower is Better):\\n")
             ws_mean = custom_metrics_summary['wasserstein'].get('mean', 'N/A')
             kl_mean = custom_metrics_summary['kl_divergence'].get('mean', 'N/A')
             if isinstance(ws_mean, float):
                 f.write(f"  Average Wasserstein Distance: {ws_mean:.4f}\n")
             else:
                 f.write(f"  Average Wasserstein Distance: {ws_mean}\n")

             if isinstance(ws_mean, float):
                 f.write(f"  Average KL_Divergence: {kl_mean:.4f}\n")
             else:
                 f.write(f"  Average Kl_Divergence: {kl_mean}\n")
             f.write(f"\\nSummary Stats (Wasserstein):\\n")
             for key, val in custom_metrics_summary['wasserstein'].items():
                 f.write(f"  {key.capitalize()}: {val if val is None or isinstance(val, str) else f'{val:.4f}'}\\n")
             f.write(f"\\nSummary Stats (KL Divergence):\\n")
             for key, val in custom_metrics_summary['kl_divergence'].items():
                 f.write(f"  {key.capitalize()}: {val if val is None or isinstance(val, str) else f'{val:.4f}'}\\n")
        logger.info(f"Custom metrics summary saved to: {metrics_summary_file}")
        print(f"Custom metrics summary saved to: {metrics_summary_file}")

        metrics_df = pd.DataFrame.from_dict(custom_metrics_results, orient='index')
        metrics_df.index.name = 'Column'
        metrics_df.to_csv(metrics_detailed_file)
        logger.info(f"Detailed custom metrics saved to: {metrics_detailed_file}")
        print(f"Detailed custom metrics saved to: {metrics_detailed_file}")

    except Exception as e:
        logger.error(f"Error during evaluation or saving metrics: {e}", exc_info=True)
        print(f"ERROR: Failed during evaluation: {e}")


    # --- Plot Generation (keep as before) ---
    if 'eval_instance' in locals():
        logger.info("Step 7: Generating Comparison Plots")
        print(f"\\n--- Generating Comparison Plots (Saving to {plots_folder}) ---")
        plot_count = 0
        error_count = 0
        # Define plot subfolder based on output file name
        plot_subfolder = os.path.join(plots_folder, f"{base_filename}_{model_type}_plots")
        os.makedirs(plot_subfolder, exist_ok=True) # Ensure subfolder exists

        for column in eval_instance.common_columns:
            try:
                 fig = eval_instance.create_distribution_plot(column)
                 if fig:
                     plot_filename = os.path.join(plot_subfolder, f"dist_{column}.html") # Save in subfolder
                     fig.write_html(plot_filename)
                     plot_count += 1
                 else:
                     logger.warning(f"Skipped plot for column '{column}' (no figure generated).")
                     print(f"Skipped plot for column '{column}' (no figure generated).")
                     error_count +=1
            except Exception as e:
                logger.error(f"Error generating plot for column '{column}': {e}", exc_info=True)
                print(f"Error generating plot for column '{column}': {e}")
                error_count += 1
        logger.info(f"Generated and saved {plot_count} plots to {plot_subfolder}. Encountered {error_count} errors/skips.")
        print(f"Generated and saved {plot_count} plots to {plot_subfolder}. Encountered {error_count} errors/skips.")
    else:
        logger.warning("Skipping plot generation because evaluation failed.")


    # --- Final Messages (update paths) ---
    logger.info("Main script execution finished.")
    print(f"\\nProcess completed for file: {os.path.basename(file_path)}")
    print(f"Synthetic dataset available at: {synthetic_data_path}")
    if 'plot_subfolder' in locals(): print(f"Evaluation plots available in: {plot_subfolder}")
    if 'metrics_path' in locals(): print(f"Evaluation metrics available in: {metrics_path}")


if __name__ == "__main__":
    main()