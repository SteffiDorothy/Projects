# src/utils.py
import pandas as pd
import logging
from typing import Optional, Dict, Any, Union # Added Dict, Any, Union
import os
import csv # Ensure csv is imported for save_csv quoting

logger = logging.getLogger(__name__)

# --- Function to save CSV ---
def save_csv(dataframe: pd.DataFrame, path: str) -> None:
    """Saves a DataFrame to a CSV file with improved error handling."""
    logger.info(f"Attempting to save DataFrame to CSV at: '{path}'")
    if dataframe is None:
        logger.error(f"Attempted to save a None DataFrame to '{path}'. Aborting.")
        raise ValueError("Cannot save a None DataFrame.")
    if dataframe.empty:
        logger.warning(f"Attempting to save an empty DataFrame to '{path}'. Proceeding.")

    logger.debug(f"DataFrame shape: {dataframe.shape}")

    try:
        output_dir = os.path.dirname(path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            logger.debug(f"Ensured output directory exists: '{output_dir}'")
    except OSError as dir_err:
        logger.error(f"Could not create directory for '{path}'. Error: {dir_err}", exc_info=True)
        raise

    try:
        dataframe.to_csv(path, index=False, encoding='utf-8', quoting=csv.QUOTE_MINIMAL) # Use standard utf-8 and minimal quoting
        logger.info(f"DataFrame successfully saved to {path}")
        print(f"File saved at {path}")
    except OSError as os_err:
        logger.error(f"OS error saving DataFrame to CSV at '{path}': {os_err}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving DataFrame to CSV at '{path}': {e}", exc_info=True)
        raise

# --- Function to load CSV ---
def load_csv(path: str) -> Optional[pd.DataFrame]:
    """Loads a DataFrame from a CSV file with improved error handling. Returns None if file not found."""
    logger.info(f"Attempting to load DataFrame from CSV at: '{path}'")
    if not os.path.isfile(path):
        logger.error(f"CSV file not found at '{path}'.")
        return None
    try:
        df = pd.read_csv(path, skipinitialspace=True) # Add skipinitialspace for potentially cleaner data
        logger.info(f"DataFrame successfully loaded from {path}, shape: {df.shape}")
        print(f"File loaded from {path}")
        return df
    except FileNotFoundError: # Redundant check
        logger.error(f"CSV file not found at '{path}'.")
        return None
    except pd.errors.EmptyDataError:
        logger.error(f"CSV file at '{path}' is empty.")
        return None
    except pd.errors.ParserError:
        logger.error(f"Error parsing CSV file at '{path}'. Check file format and delimiter.", exc_info=True)
        raise
    except OSError as os_err:
        logger.error(f"OS error loading DataFrame from CSV at '{path}': {os_err}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading DataFrame from CSV at '{path}': {e}", exc_info=True)
        raise

# --- Function to load JSON ---
def load_json(path: str, **kwargs: Any) -> Optional[pd.DataFrame]:
    """
    Loads data from a JSON file into a DataFrame.

    Args:
        path (str): Path to the JSON file.
        **kwargs: Additional keyword arguments to pass to pandas.read_json
                  (e.g., orient='records', lines=True). See pandas docs.

    Returns:
        Optional[pd.DataFrame]: Loaded DataFrame, or None if file not found/error occurs.
    """
    logger.info(f"Attempting to load DataFrame from JSON at: '{path}'")
    if not os.path.isfile(path):
        logger.error(f"JSON file not found at '{path}'.")
        return None

    try:
        orient_arg = kwargs.pop('orient', 'records')
        df = pd.read_json(path, orient=orient_arg, **kwargs)
        logger.info(f"DataFrame successfully loaded from JSON {path}, shape: {df.shape}")
        print(f"File loaded from {path}")
        return df
    except FileNotFoundError:
        logger.error(f"JSON file not found at '{path}'.")
        return None
    except ValueError as ve:
        logger.error(f"Error parsing JSON file at '{path}'. Check format and 'orient'/'lines' parameter. Error: {ve}", exc_info=True)
        raise
    except PermissionError:
        logger.error(f"Permission denied loading JSON file: '{path}'", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading DataFrame from JSON at '{path}': {e}", exc_info=True)
        raise

# --- Function to load Excel ---
def load_excel(path: str, sheet_name: Union[str, int, None] = 0, **kwargs: Any) -> Optional[pd.DataFrame]:
    """
    Loads data from an Excel file (.xlsx, .xls) into a DataFrame.
    Requires the 'openpyxl' (for .xlsx) or 'xlrd' (for .xls) library.

    Args:
        path (str): Path to the Excel file.
        sheet_name (Union[str, int, None], optional): Specific sheet to load. Defaults to 0.
        **kwargs: Additional keyword arguments to pass to pandas.read_excel.

    Returns:
        Optional[pd.DataFrame]: Loaded DataFrame, or None if file not found/error occurs.
    """
    logger.info(f"Attempting to load DataFrame from Excel at: '{path}' (sheet: {sheet_name})")
    if not os.path.isfile(path):
        logger.error(f"Excel file not found at '{path}'.")
        return None

    if sheet_name is None:
         logger.error("Loading all sheets (sheet_name=None) is not supported by this function. Please specify a sheet name or index.")
         return None

    try:
        df = pd.read_excel(path, sheet_name=sheet_name, **kwargs)
        logger.info(f"DataFrame successfully loaded from Excel {path} (sheet: {sheet_name}), shape: {df.shape}")
        print(f"File loaded from {path} (Sheet: {sheet_name})")
        return df
    except FileNotFoundError:
        logger.error(f"Excel file not found at '{path}'.")
        return None
    except ImportError as ie:
         logger.error(f"Missing necessary library to read Excel file '{path}'. Please install 'openpyxl' (for .xlsx) or 'xlrd' (for .xls). Error: {ie}", exc_info=True)
         if path.lower().endswith('.xlsx'): print("ERROR: Missing library. Please run: pip install openpyxl")
         elif path.lower().endswith('.xls'): print("ERROR: Missing library. Please run: pip install xlrd")
         return None
    except ValueError as ve:
         logger.error(f"Error reading Excel file '{path}'. Check sheet name ('{sheet_name}') or file integrity. Error: {ve}", exc_info=True)
         raise
    except PermissionError:
        logger.error(f"Permission denied loading Excel file: '{path}'", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading DataFrame from Excel at '{path}': {e}", exc_info=True)
        raise