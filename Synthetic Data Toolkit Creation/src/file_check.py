# Module: file_check.py
# Description: Handles file discovery, delimiter detection, and format conversion for CSV files.
# Refactored to use instance methods.

import csv
import os
import pandas as pd
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class FileCheck:

    def __init__(self):
        """Initializes the FileCheck instance."""
        logger.debug("FileCheck instance created.")
        pass

    # --- UPDATED: Find latest supported data file ---
    def get_latest_data_file(self, directory: str, extensions: list = ['.csv', '.json', '.xlsx', '.xls']) -> Optional[str]:
        """
        Finds the most recent file in a directory with one of the specified extensions.

        Args:
            directory (str): The directory path to search within.
            extensions (list): List of allowed file extensions (lowercase, with dot).

        Returns:
            Optional[str]: The full path to the latest supported file, or None.
        """
        logger.info(f"Searching for latest data file with extensions {extensions} in directory: '{directory}'")
        # Ensure extensions are lowercase for comparison
        allowed_extensions = [ext.lower() for ext in extensions]

        try:
            if not os.path.isdir(directory):
                 logger.error(f"Directory not found or is not a directory: {directory}")
                 return None

            # Find all files matching the allowed extensions
            supported_files = []
            for f in os.listdir(directory):
                file_path = os.path.join(directory, f)
                if os.path.isfile(file_path):
                    file_ext = os.path.splitext(f)[1].lower()
                    if file_ext in allowed_extensions:
                        supported_files.append(file_path)

            if not supported_files:
                logger.warning(f"No files with extensions {extensions} found in '{directory}'.")
                return None

            # Sort by modification time (newest file first)
            latest_file = max(supported_files, key=os.path.getmtime)
            logger.info(f"Latest data file found: '{latest_file}'")
            return latest_file
        except PermissionError:
             logger.error(f"Permission denied while accessing directory: '{directory}'", exc_info=True)
             return None
        except Exception as e:
            logger.error(f"Unexpected error searching for latest data file in '{directory}': {e}", exc_info=True)
            return None


    def detect_delimiter(self, file_path: str) -> Optional[str]:
        """
        Detects the delimiter used in a CSV file using csv.Sniffer and pandas fallback.
        Returns the detected delimiter or None if detection fails.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            Optional[str]: The detected delimiter (e.g., ',', ';') or None.
        """
        logger.debug(f"Detecting delimiter for file: '{file_path}'")
        if not os.path.isfile(file_path):
             logger.error(f"File not found for delimiter detection: '{file_path}'")
             return None

        try:
            # Attempt detection using csv.Sniffer first
            with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile: # Use utf-8-sig to handle potential BOM
                # Read a sample for sniffing
                sample = csvfile.read(2048) # Increased sample size
                if not sample:
                     logger.warning(f"File is empty, cannot detect delimiter: {file_path}")
                     return None
                # Provide common delimiters explicitly for robustness
                dialect = csv.Sniffer().sniff(sample, delimiters=[',', ';', '\t', '|'])
                logger.info(f"Detected delimiter '{dialect.delimiter}' for '{file_path}' using csv.Sniffer.")
                return dialect.delimiter
        except (csv.Error, UnicodeDecodeError) as sniff_err:
             logger.warning(f"Could not determine delimiter for '{file_path}' using csv.Sniffer (Error: {sniff_err}). Attempting fallback with pandas.")
             # Fallback using pandas (might be slower but sometimes more robust)
             try:
                 # Read just the header or first few rows with python engine guessing separator
                 # Using iterator=True and chunksize avoids loading the whole file for large files
                 df_peek = pd.read_csv(file_path, sep=None, iterator=True, chunksize=5, engine='python', encoding='utf-8-sig', skipinitialspace=True)
                 # Need to actually get a chunk to trigger detection
                 df_chunk = df_peek.get_chunk()
                 # Get the detected separator from the engine options
                 detected_sep = df_peek._engine.options.get('sep') if hasattr(df_peek._engine, 'options') else None
                 df_peek.close() # Close the iterator

                 if detected_sep:
                      logger.info(f"Detected delimiter '{detected_sep}' using pandas fallback for '{file_path}'.")
                      return detected_sep
                 else:
                      logger.warning(f"Pandas fallback could not detect delimiter for '{file_path}'.")
                      return None
             except Exception as pd_err:
                  logger.error(f"Error during pandas delimiter detection fallback for '{file_path}': {pd_err}", exc_info=True)
                  return None
        except PermissionError:
             logger.error(f"Permission denied opening file for delimiter detection: '{file_path}'", exc_info=True)
             return None
        except Exception as e:
             logger.error(f"Unexpected error during delimiter detection for '{file_path}': {e}", exc_info=True)
             return None

    def convert_to_comma_delimited(self, file_path: str) -> bool:
        """
        Converts a CSV file to comma-separated format using Pandas if needed.
        Uses detected delimiter for reading and standard comma for writing.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            bool: True if conversion was successful or not needed, False otherwise.
        """
        logger.info(f"Checking delimiter for conversion: '{file_path}'")
        try:
            detected_delimiter = self.detect_delimiter(file_path) # Call instance method

            if detected_delimiter is None:
                 logger.error(f"Could not detect delimiter for '{file_path}'. Cannot check/convert.")
                 return False # Indicate failure

            if detected_delimiter == ',':
                logger.info(f"File '{file_path}' is already comma-delimited. No conversion needed.")
                return True # Indicate success (no action needed)

            # Proceed with conversion if delimiter is not comma
            logger.info(f"Converting '{file_path}' from delimiter '{detected_delimiter}' to comma-delimited format...")
            print(f"Converting {os.path.basename(file_path)} to comma-delimited format...") # Keep user print, maybe just filename

            # Read using detected delimiter, write using comma
            # Read as strings initially ('object' dtype) for safety during re-writing, avoids type inference issues
            df = pd.read_csv(file_path, delimiter=detected_delimiter, dtype='object', encoding='utf-8-sig', skipinitialspace=True)
            # Write using standard comma delimiter and minimal quoting
            df.to_csv(file_path, index=False, encoding='utf-8', quoting=csv.QUOTE_MINIMAL)
            logger.info(f"File successfully converted to comma-delimited: {file_path}")
            print(f"File successfully converted: {os.path.basename(file_path)}") # Keep user print
            return True # Indicate success

        except PermissionError:
            logger.error(f"Permission denied during conversion for file: '{file_path}'", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Error during delimiter detection or conversion for '{file_path}': {e}", exc_info=True)
            return False # Indicate failure