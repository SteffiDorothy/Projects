# src/privacy_utils.py
# Description: Utility class for applying privacy-preserving transformations,
# including hashing and differential privacy (Laplace noise).

import hashlib
import re
import pandas as pd
import numpy as np # Needed for differential privacy
import logging

logger = logging.getLogger(__name__)

class PrivacyUtils:

    def __init__(self):
        """Initializes the PrivacyUtils instance."""
        # No instance state needed for now, but provides proper object structure.
        logger.debug("PrivacyUtils instance created.")
        pass

    # --- Hashing Methods ---

    def hashstring(self, value: str) -> str:
        """
        Hashes a string using SHA-256.

        Parameters:
            value (str): The original string to hash.

        Returns:
            str: The full-length SHA-256 hash.
        """
        # No logging needed here as it's a low-level helper called many times
        return hashlib.sha256(value.encode()).hexdigest()

    def truncator(self, original: str, hashed: str) -> str:
        """
        Truncates the hash to match the original string's length.

        Parameters:
            original (str): The original string.
            hashed (str): The hashed string.

        Returns:
            str: The truncated hash.
        """
        # No logging needed here either
        return hashed[:len(original)]

    def apply_hashing(self, data: pd.DataFrame, pii_columns: list) -> pd.DataFrame:
        """
        Applies hashing to specified PII columns using unique-value mapping.

        Parameters:
            data (pd.DataFrame): The input dataset.
            pii_columns (list): List of column names to hash.

        Returns:
            pd.DataFrame: Modified dataset with hashed PII values.
        """
        logger.info(f"Starting hashing process for columns: {pii_columns}")
        if not pii_columns:
            logger.warning("No columns provided for hashing. Returning original data.")
            return data

        data_copy = data.copy() # Work on a copy
        processed_count = 0
        error_cols = []

        for col in pii_columns:
            if col in data_copy.columns:
                logger.debug(f"Processing column '{col}' for hashing.")
                try:
                    unique_values = data_copy[col].dropna().unique()
                    value_map = {}

                    for val in unique_values:
                        str_val = str(val)
                        hashed = self.hashstring(str_val)
                        truncated = self.truncator(str_val, hashed)
                        value_map[val] = truncated

                    original_col = data_copy[col]  # Keep original for non-matched/NaN values
                    string_col = original_col.astype(str)
                    hashed_col = string_col.map(value_map)

                    # Use .map for potentially faster application than lambda
                    data_copy[col] = hashed_col.combine_first(original_col) # Preserve NaN

                    processed_count += 1
                    logger.debug(f"Successfully hashed column '{col}'.")

                except Exception as e:
                    logger.error(f"Error hashing column '{col}': {e}", exc_info=True) # Log stack trace
                    error_cols.append(col)

            else:
                logger.warning(f"Column '{col}' specified for hashing not found in DataFrame.")

        logger.info(f"Hashing process finished. Processed {processed_count} columns.")
        if error_cols:
            logger.warning(f"Errors occurred while hashing columns: {error_cols}")
        return data_copy

    # --- Differential Privacy Methods (Merged from differential_privacy.py) ---

    def add_laplace_noise(self, data: pd.DataFrame, columns: list, epsilon: float = 1.0) -> pd.DataFrame:
        """
        Adds Laplace noise to specified numerical columns for differential privacy.

        Parameters:
            data (pd.DataFrame): Input data.
            columns (list): List of numerical column names to apply noise to.
            epsilon (float): Privacy budget (smaller = more private, must be > 0).

        Returns:
            pd.DataFrame: Data with added noise.
        """
        logger.info(f"Starting Laplace noise addition for columns: {columns} with epsilon={epsilon}")
        if not columns:
            logger.warning("No columns provided for Laplace noise. Returning original data.")
            return data
        if epsilon <= 0:
            logger.error(f"Epsilon must be positive, but got {epsilon}. Returning original data.")
            # Consider raising ValueError("Epsilon must be positive")
            return data # Or raise ValueError

        noisy_data = data.copy()
        processed_count = 0
        error_cols = []

        for col in columns:
            if col in noisy_data.columns:
                logger.debug(f"Processing column '{col}' for Laplace noise.")
                try:
                    # Ensure the column is numeric before proceeding
                    if not pd.api.types.is_numeric_dtype(noisy_data[col]):
                        logger.warning(f"Column '{col}' is not numeric. Skipping Laplace noise addition.")
                        error_cols.append(col)
                        continue

                    # Select non-NaN numeric data for calculations
                    col_data_numeric = noisy_data[col].dropna()
                    if col_data_numeric.empty:
                         logger.warning(f"Column '{col}' contains only NaN values or is empty after dropna. Skipping.")
                         continue

                    # Calculate sensitivity (using range for simplicity, consider alternatives for robustness)
                    # Ensure calculation happens on numeric data
                    sensitivity = col_data_numeric.astype(float).max() - col_data_numeric.astype(float).min()

                    # Handle zero sensitivity case (all values are the same)
                    if sensitivity == 0 or pd.isna(sensitivity):
                         logger.warning(f"Column '{col}' has zero or NaN sensitivity (e.g., all values identical or NaNs). Skipping noise addition.")
                         continue # Avoid division by zero or adding noise

                    scale = sensitivity / epsilon
                    logger.debug(f"Calculated scale for '{col}': sensitivity={sensitivity}, epsilon={epsilon}, scale={scale}")

                    # Generate noise only for non-NaN values' indices
                    noise = np.random.laplace(0, scale, len(col_data_numeric))

                    # Add noise only to the non-NaN values using their index
                    # Ensure noise is added to float version to avoid type issues
                    noisy_data.loc[col_data_numeric.index, col] = noisy_data.loc[col_data_numeric.index, col].astype(float) + noise
                    processed_count += 1
                    logger.debug(f"Successfully added Laplace noise to column '{col}'.")

                except Exception as e:
                    logger.error(f"Error adding Laplace noise to column '{col}': {e}", exc_info=True)
                    error_cols.append(col)
            else:
                logger.warning(f"Column '{col}' specified for Laplace noise not found in DataFrame.")

        logger.info(f"Laplace noise addition finished. Processed {processed_count} columns.")
        if error_cols:
            logger.warning(f"Issues occurred while adding noise to columns: {error_cols}")
        return noisy_data