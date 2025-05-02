# src/hyperparameter_tuning.py
import streamlit as st
import pandas as pd
from typing import Dict, Any, Tuple
import logging

# Import the helper function from config
from src.config import get_default_hyperparameters

logger = logging.getLogger(__name__)

class HyperparameterTuning:

    # display_tuning_options remains the same as the previous version...
    @staticmethod
    def display_tuning_options(model_type: str) -> None: # Return None explicitly
        """
        Display hyperparameter tuning options in the Streamlit UI,
        using defaults loaded from the configuration.
        """
        st.markdown("### Hyperparameter Tuning")

        # Load default parameters for the selected model type from config
        try:
            default_params = get_default_hyperparameters(model_type)
            logger.debug(f"Loaded default params for UI ({model_type}): {default_params}")
        except Exception as e:
            logger.error(f"Failed to load default hyperparameters for {model_type} from config: {e}", exc_info=True)
            st.error(f"Error loading default config for {model_type}. Using fallback values.")
            # Define minimal fallbacks if config loading fails
            if model_type == 'TVAE':
                default_params = {'embedding_dim': 128, 'compress_dims': (128, 128), 'decompress_dims': (128, 128), 'batch_size': 500, 'epochs': 300, 'l2scale': 1e-5} # Add l2scale fallback
            elif model_type == 'CTGAN':
                default_params = {'generator_dim': (256, 256), 'discriminator_dim': (256, 256), 'generator_lr': 2e-4, 'discriminator_lr': 2e-4, 'batch_size': 500, 'epochs': 300, 'generator_decay': 1e-6, 'discriminator_decay': 1e-6} # Add decays
            elif model_type == 'GaussianCopula':
                default_params = {'default_distribution': 'beta'}
            else:
                default_params = {}

        # Add general hyperparameter tuning explanation
        with st.expander("ℹ️ What is Hyperparameter Tuning?"):
            st.markdown("""
                Hyperparameter tuning is the process of finding the optimal settings for a machine learning model.
                These parameters control the learning process and model architecture, affecting:
                - How well the model learns from the training data
                - How well it generates new, realistic synthetic data
                - The trade-off between training speed and model quality
            """)

        # --- TVAE Tuning Options ---
        if model_type == 'TVAE':
            st.markdown("#### TVAE (Tabular Variational Autoencoder) Parameters")
            with st.expander("ℹ️ About TVAE Parameters"):
                st.markdown("""
                    TVAE uses a neural network architecture to learn and generate tabular data:
                    - Larger dimensions generally mean better quality but slower training.
                    - Batch size affects memory usage and training stability.
                    - More epochs mean better learning but longer training time.
                """)

            # Use .get() with fallback values matching the expected type if key is missing in config
            st.number_input(
                "Embedding Dimensions",
                min_value=16, max_value=1024, # Wider range
                value=int(default_params.get('embedding_dim', 128)), # Ensure int
                key='tvae_embedding_dim', # Use model-specific keys
                help="Size of the latent space representation. Larger values capture more complex patterns but need more data/time. Default from config."
            )

            # Get tuple default, convert to string for text input
            compress_dims_default = default_params.get('compress_dims', (128, 128))
            st.text_input(
                "Compress Dimensions (Encoder)",
                value=str(compress_dims_default), # Display as string "(128, 128)"
                key='tvae_compress_dims',
                help="Defines the architecture of the encoder network layers. Format: (dim1, dim2, ...). Default from config."
            )

            decompress_dims_default = default_params.get('decompress_dims', (128, 128))
            st.text_input(
                "Decompress Dimensions (Decoder)",
                value=str(decompress_dims_default), # Display as string "(128, 128)"
                key='tvae_decompress_dims',
                help="Defines the architecture of the decoder network layers. Format: (dim1, dim2, ...). Default from config."
            )

            st.number_input(
                "Batch Size",
                min_value=32, max_value=1024, # Wider range
                value=int(default_params.get('batch_size', 500)), # Ensure int
                step=100, # Adjust step maybe
                key='tvae_batch_size',
                help="Number of samples processed before model update. Larger batches more stable but use more memory. Default from config."
            )

            st.number_input(
                "Number of Epochs",
                min_value=10, max_value=1000, # Wider range
                value=int(default_params.get('epochs', 300)), # Ensure int
                step=50,
                key='tvae_epochs',
                help="Number of complete passes through the training data. More epochs generally mean better results but longer training time. Default from config."
            )
            # Optionally add l2scale input if desired
            # st.number_input("L2 Regularization (Weight Decay)", min_value=0.0, max_value=1e-2,
            #                 value=float(default_params.get('l2scale', 1e-5)), format="%.1e", step=1e-6,
            #                 key='tvae_l2scale', help="...")


        # --- CTGAN Tuning Options ---
        elif model_type == 'CTGAN':
            st.markdown("#### CTGAN (Conditional Tabular GAN) Parameters")
            with st.expander("ℹ️ About CTGAN Parameters"):
                 st.markdown("""
                    CTGAN uses a conditional GAN architecture specifically designed for tabular data:
                    - Generator dimensions affect the model's capacity to learn complex patterns.
                    - Discriminator dimensions control how well the model distinguishes real from fake data.
                    - Learning rates balance training stability and speed.
                    - Batch size must be a multiple of 'pac' (usually 10).
                """)

            generator_dim_default = default_params.get('generator_dim', (256, 256))
            st.text_input(
                "Generator Dimensions",
                value=str(generator_dim_default),
                key='ctgan_generator_dim',
                help="Architecture of the generator network layers. Format: (dim1, dim2, ...). Default from config."
            )

            discriminator_dim_default = default_params.get('discriminator_dim', (256, 256))
            st.text_input(
                "Discriminator Dimensions",
                value=str(discriminator_dim_default),
                key='ctgan_discriminator_dim',
                help="Architecture of the discriminator network layers. Format: (dim1, dim2, ...). Default from config."
            )

            st.number_input(
                "Generator Learning Rate",
                min_value=1e-6, max_value=1e-2, # Wider range
                value=float(default_params.get('generator_lr', 2e-4)), # Ensure float
                format="%.1e", # Use scientific notation for better display
                step=1e-5,
                key='ctgan_generator_lr',
                help="Controls how quickly the generator updates. Lower values are more stable but slower. Default from config."
            )

            st.number_input(
                "Discriminator Learning Rate",
                min_value=1e-6, max_value=1e-2, # Wider range
                value=float(default_params.get('discriminator_lr', 2e-4)), # Ensure float
                format="%.1e",
                step=1e-5,
                key='ctgan_discriminator_lr',
                help="Controls how quickly the discriminator updates. Lower values are more stable but slower. Default from config."
            )

            pac_value = int(default_params.get('pac', 10)) # Ensure int
            st.number_input(
                "Batch Size",
                min_value=pac_value, max_value=1000, # Min value is pac
                value=int(default_params.get('batch_size', 500)), # Ensure int
                step=pac_value, # Step must be multiple of pac
                key='ctgan_batch_size',
                help=f"⚠️ Must be a multiple of pac (default={pac_value}). Number of samples per update. Default from config."
            )

            st.number_input(
                "Number of Epochs",
                min_value=10, max_value=1000, # Wider range
                value=int(default_params.get('epochs', 300)), # Ensure int
                step=50,
                key='ctgan_epochs',
                help="Number of complete passes through the training data. More epochs generally mean better results but longer training time. Default from config."
            )
            # Add other CTGAN params if needed (generator_decay, discriminator_decay, pac, cuda) ensuring type

        # --- Gaussian Copula Tuning Options ---
        elif model_type == 'GaussianCopula':
            st.markdown("#### Gaussian Copula Parameters")
            with st.expander("ℹ️ About Gaussian Copula Parameters"):
                 st.markdown("""
                    Gaussian Copula is a statistical method that models dependencies using correlations:
                    - Distribution type affects how individual numerical columns are modeled.
                    - Generally faster than neural network approaches. Fewer tunable parameters directly in the model itself (most tuning is via metadata).
                """)

            dist_options = ['beta', 'gaussian', 'gamma', 'gaussian_kde', 'histogram', 'kde', 'log_laplace', 'log_normal', 'laplace', 'student_t', 'truncated_gaussian', 'uniform', 'weibull']
            default_dist = str(default_params.get('default_distribution', 'beta')) # Ensure string for comparison/index
            st.selectbox(
                "Default Numerical Distribution",
                options=dist_options,
                index=dist_options.index(default_dist) if default_dist in dist_options else 0, # Find index of default
                key='gc_default_distribution',
                help="The probability distribution used by default to model numerical columns (can be overridden per column in metadata). Default from config."
            )


    @staticmethod
    def get_tuned_params(model_type: str) -> Dict[str, Any]:
        """
        Get the tuned parameters selected by the user from the Streamlit session state.
        Ensures correct data types for numeric parameters.
        Handles potential conversion errors for text inputs representing tuples.
        """
        tuned_params = {}
        logger.debug(f"Retrieving tuned parameters for {model_type} from session state.")

        def safe_eval_tuple(key: str, default: Tuple) -> Tuple:
            """Safely evaluate string input as tuple, fallback to default."""
            val_str = st.session_state.get(key, str(default))
            try:
                evaluated = eval(val_str)
                if isinstance(evaluated, tuple):
                    return evaluated
                elif isinstance(evaluated, list): # Allow lists too
                     return tuple(evaluated)
                else:
                    logger.warning(f"Input for {key} ('{val_str}') did not evaluate to a tuple/list. Using default {default}.")
                    return default
            except Exception as e:
                logger.warning(f"Error evaluating input for {key} ('{val_str}'): {e}. Using default {default}.")
                return default

        # Helper to safely get and cast session state values
        def get_state_value(key: str, default: Any, cast_type: type):
            value = st.session_state.get(key, default)
            try:
                return cast_type(value)
            except (ValueError, TypeError) as e:
                logger.warning(f"Could not cast session state value for key '{key}' (value: {value}) to {cast_type}. Using default {default}. Error: {e}")
                return default

        if model_type == 'TVAE':
            # Get defaults again to use as fallbacks in get_state_value
            defaults = get_default_hyperparameters(model_type)
            tuned_params = {
                # --- MODIFICATION START: Explicit Casting ---
                'embedding_dim': get_state_value('tvae_embedding_dim', defaults.get('embedding_dim', 128), int),
                'compress_dims': safe_eval_tuple('tvae_compress_dims', defaults.get('compress_dims', (128, 128))),
                'decompress_dims': safe_eval_tuple('tvae_decompress_dims', defaults.get('decompress_dims', (128, 128))),
                'batch_size': get_state_value('tvae_batch_size', defaults.get('batch_size', 500), int),
                'epochs': get_state_value('tvae_epochs', defaults.get('epochs', 300), int)
                # If l2scale UI was added:
                # 'l2scale': get_state_value('tvae_l2scale', defaults.get('l2scale', 1e-5), float)
                # --- MODIFICATION END ---
            }

        elif model_type == 'CTGAN':
            defaults = get_default_hyperparameters(model_type)
            tuned_params = {
                # --- MODIFICATION START: Explicit Casting ---
                'generator_dim': safe_eval_tuple('ctgan_generator_dim', defaults.get('generator_dim', (256, 256))),
                'discriminator_dim': safe_eval_tuple('ctgan_discriminator_dim', defaults.get('discriminator_dim', (256, 256))),
                'generator_lr': get_state_value('ctgan_generator_lr', defaults.get('generator_lr', 2e-4), float),
                'discriminator_lr': get_state_value('ctgan_discriminator_lr', defaults.get('discriminator_lr', 2e-4), float),
                'batch_size': get_state_value('ctgan_batch_size', defaults.get('batch_size', 500), int),
                'epochs': get_state_value('ctgan_epochs', defaults.get('epochs', 300), int)
                # Add other CTGAN params (decays etc.) with casting if UI added
                # --- MODIFICATION END ---
            }
            # Ensure batch_size is adjusted if needed (redundant if input enforces step, but safe)
            pac = int(defaults.get('pac', 10)) # Ensure pac is int
            if tuned_params['batch_size'] % pac != 0:
                 original_bs = tuned_params['batch_size']
                 tuned_params['batch_size'] = ((original_bs // pac) + (1 if original_bs % pac != 0 else 0)) * pac
                 logger.warning(f"Adjusting tuned CTGAN batch_size {original_bs} to multiple of pac={pac}: {tuned_params['batch_size']}")


        elif model_type == 'GaussianCopula':
             defaults = get_default_hyperparameters(model_type)
             tuned_params = {
                 # --- MODIFICATION START: Explicit Casting (ensure string) ---
                 'default_distribution': get_state_value('gc_default_distribution', defaults.get('default_distribution', 'beta'), str),
                 # --- MODIFICATION END ---
             }

        logger.debug(f"Retrieved and cast tuned params for {model_type}: {tuned_params}")
        return tuned_params