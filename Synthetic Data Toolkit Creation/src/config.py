# src/config.py
import yaml
import os
from typing import Dict, Any, Optional, Tuple, List, Union # Import more types
import logging

logger = logging.getLogger(__name__)

CONFIG_FILE_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')

# --- Type Casting Helper ---
def _cast_hyperparameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively cast known hyperparameter types."""
    casted_params = {}
    # Define expected types (add more as needed)
    type_map = {
        'embedding_dim': int,
        'batch_size': int,
        'epochs': int,
        'loss_factor': int,
        'pac': int,
        'l2scale': float,
        'generator_lr': float,
        'generator_decay': float,
        'discriminator_lr': float,
        'discriminator_decay': float,
        'epsilon': float, # For potential future DP config
        'cuda': bool,
        # Dimensions should be tuples of ints
        'compress_dims': tuple,
        'decompress_dims': tuple,
        'generator_dim': tuple,
        'discriminator_dim': tuple,
        # Default distribution is string
        'default_distribution': str,
    }

    for key, value in params.items():
        target_type = type_map.get(key)
        if target_type:
            try:
                if target_type is tuple and isinstance(value, list):
                    # Ensure elements within tuple are ints if it's a dimension tuple
                    if key in ['compress_dims', 'decompress_dims', 'generator_dim', 'discriminator_dim']:
                         casted_params[key] = tuple(int(i) for i in value)
                    else:
                         casted_params[key] = tuple(value) # Generic list to tuple
                elif target_type is bool:
                     # Handle potential string representations of bool
                     if isinstance(value, str):
                          if value.lower() in ['true', 'yes', '1']:
                               casted_params[key] = True
                          elif value.lower() in ['false', 'no', '0']:
                               casted_params[key] = False
                          else:
                               raise ValueError(f"Invalid boolean string: {value}")
                     else:
                          casted_params[key] = bool(value)
                elif target_type in [int, float, str]:
                     casted_params[key] = target_type(value)
                else: # Fallback for unexpected target_type
                     casted_params[key] = value
            except (ValueError, TypeError) as e:
                logger.warning(f"Could not cast hyperparameter '{key}' (value: {value}, type: {type(value)}) to {target_type}. Keeping original. Error: {e}")
                casted_params[key] = value # Keep original on casting error
        else:
            # If key not in type_map, keep original value
            casted_params[key] = value

    return casted_params


# --- Configuration Loading ---
def load_config(path: str = CONFIG_FILE_PATH) -> Dict[str, Any]:
    """Loads configuration settings from the YAML file and casts hyperparameter types."""
    # Define default structure with expected types where possible
    default_config = {
        'paths': {
            'data_folder': "./data", 'output_folder': "./output", 'models_folder': "./models",
            'plots_folder_name': "plots", 'metrics_folder_name': "metrics"
        },
        'filenames': {
            'synthetic_data': "synthetic_data.csv", 'metadata': "metadata.json", 'model': "synthesizer.pkl"
        },
        'hyperparameters': {
            'TVAE': { 'embedding_dim': 128, 'compress_dims': (128, 128), 'decompress_dims': (128, 128), 'l2scale': 1e-5, 'batch_size': 500, 'epochs': 300, 'loss_factor': 2, 'cuda': False },
            'CTGAN': { 'embedding_dim': 128, 'generator_dim': (256, 256), 'discriminator_dim': (256, 256), 'generator_lr': 2e-4, 'generator_decay': 1e-6, 'discriminator_lr': 2e-4, 'discriminator_decay': 1e-6, 'batch_size': 500, 'epochs': 300, 'pac': 10, 'cuda': False },
            'GaussianCopula': { 'default_distribution': 'beta' }
        }
    }
    try:
        with open(path, 'r') as f:
            config_data = yaml.safe_load(f)
            if not isinstance(config_data, dict): # Check if file is completely invalid
                 logger.warning(f"Configuration file {path} is empty or invalid YAML structure. Using defaults.")
                 return default_config

            # Ensure top-level keys exist, falling back section by section
            config_data['paths'] = config_data.get('paths', default_config['paths'])
            config_data['filenames'] = config_data.get('filenames', default_config['filenames'])
            loaded_hyperparams = config_data.get('hyperparameters', default_config['hyperparameters'])

            # --- MODIFICATION START: Cast Hyperparameter types ---
            casted_hyperparams = {}
            default_models = default_config['hyperparameters']
            for model_type in default_models.keys(): # Iterate known model types
                # Get params from file or use default section if missing
                raw_params = loaded_hyperparams.get(model_type, default_models[model_type])
                # Ensure defaults are applied for missing keys within a section
                full_raw_params = default_models[model_type].copy()
                full_raw_params.update(raw_params) # Loaded values override defaults
                # Cast the types for the specific model
                casted_hyperparams[model_type] = _cast_hyperparameters(full_raw_params)
            config_data['hyperparameters'] = casted_hyperparams
            # --- MODIFICATION END ---

            return config_data
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {path}. Using default settings.")
        return default_config # Return defaults defined above
    except (yaml.YAMLError, Exception) as e: # Catch YAML parsing errors and others
        logger.error(f"Error loading or parsing config file {path}: {e}", exc_info=True)
        logger.warning("Using default settings as fallback due to error.")
        return default_config # Return defaults defined above

# Load the configuration
_config: Dict[str, Any] = load_config()

# --- Make settings easily accessible ---

# Directory Paths (remain the same)
_paths: Dict[str, Any] = _config.get('paths', {})
DATA_FOLDER: str = _paths.get('data_folder', "./data")
OUTPUT_FOLDER: str = _paths.get('output_folder', "./output")
MODELS_FOLDER: str = _paths.get('models_folder', "./models")
PLOTS: str = _paths.get('plots_folder_name', "plots")
METRICS: str = _paths.get('metrics_folder_name', "metrics")

# Filenames (remain the same)
_filenames: Dict[str, Any] = _config.get('filenames', {})
SYNTHETIC_DATA_FILENAME: str = _filenames.get('synthetic_data', "synthetic_data.csv")
METADATA_FILENAME: str = _filenames.get('metadata', "metadata.json")
MODEL_FILENAME: str = _filenames.get('model', "synthesizer.pkl")

# Default Hyperparameters - Now contains casted types
DEFAULT_HYPERPARAMETERS: Dict[str, Dict[str, Any]] = _config.get('hyperparameters', {
    'TVAE': {}, 'CTGAN': {}, 'GaussianCopula': {} # Minimal fallback
})

# --- Construct Full Paths (remain the same) ---
SYNTHETIC_DATA_PATH: str = os.path.join(OUTPUT_FOLDER, SYNTHETIC_DATA_FILENAME)
METADATA_PATH: str = os.path.join(OUTPUT_FOLDER, METADATA_FILENAME)
MODEL_PATH: str = os.path.join(MODELS_FOLDER, MODEL_FILENAME)
PLOTS_FOLDER: str = os.path.join(OUTPUT_FOLDER, PLOTS)
METRICS_PATH: str = os.path.join(OUTPUT_FOLDER, METRICS)

# Log successful loading status (remain the same)
logger.info("Configuration loaded with type casting for hyperparameters.")


# --- Helper function to get specific model hyperparameters ---
def get_default_hyperparameters(model_type: str) -> Dict[str, Any]:
    """
    Retrieves the default hyperparameters (with casted types) for a specific model type.
    """
    params = DEFAULT_HYPERPARAMETERS.get(model_type, {})
    if not params:
        logger.warning(f"No default hyperparameters found in config for model type '{model_type}'. Returning empty dict.")
    # No need to cast tuples here anymore, should be done during loading
    return params