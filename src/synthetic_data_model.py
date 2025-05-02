# Module: synthetic_data_model.py
# Description: Defines and fits a data synthesizer model, then saves the model for later use.

from sdv.single_table import GaussianCopulaSynthesizer, CTGANSynthesizer, TVAESynthesizer
from sdv.metadata import Metadata
import pandas as pd
import logging
import os
from typing import Dict, Any
from src.config import get_default_hyperparameters


logger = logging.getLogger(__name__)

class SyntheticDataModel:
    synthesizer = None

    @classmethod
    def create_model(cls, data: pd. DataFrame, metadata_path: str, model_path: str, model_type: str, **kwargs: Any):
        """
        Create and train a synthetic data model.
        
        Parameters:
            data (pd.DataFrame): Input data
            metadata_path (str): Path to metadata file
            model_path (str): Path to save the model
            model_type (str): Type of model to create
            **kwargs: Additional hyperparameters for the model
        """
        logger.info(f"Attempting to create and train model: type={model_type}, output={model_path}")
        logger.debug(f"Using metadata: {metadata_path}, data shape: {data.shape}, kwargs: {kwargs}")
        try:
            # Load metadata
            metadata = Metadata.load_from_json(metadata_path)
            logger.info(f"Metadata loaded successfully from {metadata_path}")

            # 2. Get Default Hyperparameters from Config
            default_params: Dict[str, Any] = get_default_hyperparameters(model_type)
            logger.debug(f"Loaded default parameters for {model_type} from config: {default_params}")

            final_params = default_params.copy()
            final_params.update(kwargs)  # kwargs values will overwrite defaults if keys match

            # Create model based on type
            if model_type == 'TVAE':
                cls.synthesizer = TVAESynthesizer(
                    metadata=metadata,
                    **final_params
                )
            elif model_type == 'CTGAN':
                # Ensure batch_size is multiple of pac (default pac is 10)
                pac = final_params.get("pac", 10)
                batch_size = final_params.get('batch_size', 500)
                if batch_size % pac != 0:
                    batch_size = ((batch_size // pac) + 1) * pac
                    final_params['batch_size'] = batch_size
                
                cls.synthesizer = CTGANSynthesizer(
                    metadata=metadata,
                    **final_params
                )
            elif model_type == 'GaussianCopula':
                cls.synthesizer = GaussianCopulaSynthesizer(
                    metadata=metadata,
                    **final_params
                )
            else:
                logger.error(f"Unknown model type provided: {model_type}")
                raise ValueError(f"Unknown model type: {model_type}")


            logger.info(f"Initialized synthesizer: {model_type}")

            # Fit the model
            logger.info("Starting model fitting...")
            cls.synthesizer.fit(data)
            logger.info("Model fitting completed.")
            
            # Save the model
            cls.synthesizer.save(model_path)

            # Save the model
            cls.synthesizer.save(model_path)
            logger.info(f"Model saved successfully to {model_path}")

            return cls.synthesizer

        except Exception as e:
            logger.error(f"Error creating/training model: {e}", exc_info=True)
            raise

    @classmethod
    def generate_synthetic_data(cls, num_rows: int) -> pd.DataFrame:
        """
        Generates synthetic data using the trained synthesizer.

        Parameters:
            num_rows (int): Number of synthetic rows to generate.

        Returns:
            pd.DataFrame: The generated synthetic data DataFrame.

        Raises:
            Exception: If the model is not trained or loaded before calling.
        """
        if cls.synthesizer is None:
            logger.error("Attempted to generate data before model was trained or loaded.")
            raise Exception("Model has not been trained or loaded. Call create_model or ensure model is loaded first.")

        try:
            num_rows = int(num_rows)  # Ensure num_rows is integer
            if num_rows <= 0:
                logger.error(f"Number of rows must be positive, received: {num_rows}")
                raise ValueError("Number of rows must be positive.")
        except ValueError as e:
            logger.error(f"Invalid value provided for num_rows: {num_rows}. Error: {e}")
            raise ValueError(f"Invalid number of rows: {num_rows}") from e

        logger.info(f"Generating {num_rows} synthetic rows using the current synthesizer...")
        print(f"Generating {num_rows} synthetic rows...")  # Keep user-facing print
        try:
            # Call the sample method on the stored synthesizer instance
            synthetic_data = cls.synthesizer.sample(num_rows=num_rows)
            logger.info(f"Successfully generated {len(synthetic_data)} synthetic rows.")
            return synthetic_data
        except Exception as e:
            # Catch errors during the sampling process
            logger.error(f"An unexpected error occurred during synthetic data generation: {e}", exc_info=True)
            raise  # Re-raise the exception