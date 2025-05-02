# Module: metadata_converter.py
# Description: Creates metadata from CSV data and saves it as JSON for use in data synthesis models.

import pandas as pd
from sdv.datasets.local import load_csvs
from sdv.metadata import Metadata
import logging
from typing import Optional, Dict, Any
import os

logger = logging.getLogger(__name__)

class MetadataConverter:

    def __init__(self):
        """Initializes the MetadataConverter instance."""
        # Initialize metadata as an instance variable
        self.metadata: Optional[Metadata] = None
        logger.debug("MetadataConverter instance created.")

    def create_metadata(self, data_path: str, json_output_path: str) -> None:
        """
        Creates and saves metadata from data to a JSON file.

        Parameters:
            data_path (str): Path to dataset directory containing CSVs.
            json_output_path (str): Path to save metadata JSON.

        Returns:
            None
        """
        logger.info(f"Attempting to create metadata from data in '{data_path}'...")
        logger.debug(f"Output JSON path: {json_output_path}")
        try:
            # load_csvs returns a dictionary mapping table names to dataframes
            dataframes_dict: Dict[str, pd.DataFrame] = load_csvs(folder_name=data_path)
            if not dataframes_dict:
                 logger.error(f"No CSV data found or loaded from {data_path}")
                 raise ValueError(f"No CSV data found in {data_path}")

            logger.info(f"Loaded {len(dataframes_dict)} dataframe(s) from {data_path}. Detecting metadata...")
            # Pass the dictionary directly to detect_from_dataframes
            self.metadata = Metadata.detect_from_dataframes(data=dataframes_dict)
            logger.info(f"Metadata detected successfully.")

            # Ensure output directory exists
            output_dir = os.path.dirname(json_output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            if os.path.exists(json_output_path):
                logger.warning(f"Existing metadata file found at {json_output_path}. Removing it.")
                os.remove(json_output_path)

            self.metadata.save_to_json(filepath=json_output_path) # Use 'filepath' argument
            logger.info(f"Metadata saved successfully to {json_output_path}")


        except FileNotFoundError as e:

            logger.error(f"File or Directory not found during metadata creation: {e}", exc_info=True)
            self.metadata = None  # Ensure reset on error
            raise  # Re-raise specific error

        except ValueError as e:
            logger.error(f"Value error during metadata creation (e.g., no data found): {e}", exc_info=True)
            self.metadata = None
            raise  # Re-raise specific error

        except (OSError, IOError) as e:
            logger.error(f"File system error during metadata creation/saving: {e}", exc_info=True)
            self.metadata = None
            raise IOError(f"File system error: {e}")  # Re-raise as IOError

        except Exception as e:
            # Catch other potential errors (e.g., from SDV internals)
            logger.error(f"An unexpected error occurred during metadata creation: {e}", exc_info=True)
            self.metadata = None
            raise  # Re-raise the original error

    @classmethod
    def get_metadata(self) -> Metadata:
        """
        Retrieves the metadata instance.

        Returns:
            Metadata: SDV Metadata object.

        Raises:
            Exception: If metadata is not initialized.
        """
        if self.metadata is None:
            logger.warning("Metadata accessed before creation or after an error.")
            # Raise Exception("Metadata not created. Call create_metadata first.")
            # Or return None to indicate it's not ready
            return None
        return self.metadata