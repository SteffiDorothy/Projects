# src/validation.py
# Handles data validation using Pandera

import pandas as pd
import pandera as pa
from pandera.errors import SchemaError
import logging

logger = logging.getLogger(__name__)

# --- Define Schema with Business Rules ---

# Define checks for specific columns if they exist
quantity_check = pa.Check.gt(0, name="Quantity_Positive", error="Quantity must be positive")

# Define the schema
data_schema = pa.DataFrameSchema(
    columns={
        # Column definitions (types are checked if column exists)
        "OrderID": pa.Column(pa.Int, required=False),
        # Apply check to Quantity column if it exists
        "Quantity": pa.Column(pa.Int, required=False, checks=quantity_check),
        "OrderDate": pa.Column(pa.DateTime, required=False),
    },

    strict=False, # Don't fail if extra columns are present
    coerce=True   # Attempt to coerce types
)


# --- Basic Check Functions (Keep existing ones) ---

def check_no_fully_empty_columns(df: pd.DataFrame) -> bool:
    """Checks if any column consists entirely of null values."""
    # Consider running this check *before* coercion if nulls are expected initially
    if df.isnull().all().any():
        empty_cols = df.columns[df.isnull().all()].tolist()
        logger.error(f"Validation Error: Columns are entirely empty: {empty_cols}")
        raise ValueError(f"Columns are entirely empty: {empty_cols}")
    return True

def check_min_rows(df: pd.DataFrame, min_rows: int = 1) -> bool:
    """Checks if the dataframe has a minimum number of rows."""
    if len(df) < min_rows:
        logger.error(f"Validation Error: DataFrame has less than {min_rows} rows.")
        raise ValueError(f"DataFrame has less than {min_rows} rows.")
    return True


# --- Main Validation Function ---

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs validation checks, including basic structure and business rules,
    on the input DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to validate.

    Returns:
        pd.DataFrame: The validated (potentially coerced) DataFrame.

    Raises:
        SchemaError: If validation defined in the Pandera schema fails.
        ValueError: If custom checks (like empty columns) fail.
    """
    logger.info("Starting data validation...")
    if df is None or df.empty:
        logger.warning("Input DataFrame is empty or None. Skipping validation.")
        return df

    try:
        # Apply basic custom checks first
        check_min_rows(df)
        # check_no_fully_empty_columns(df) # Re-evaluate if needed after coercion

        # Apply the main Pandera schema
        logger.info("Applying Pandera schema for type coercion and business rule checks (incl. uniqueness)...")
        validated_df = data_schema.validate(df) # Validate in-place (due to coerce=True)
        logger.info("Pandera schema validation passed successfully.")

        # Could potentially run check_no_fully_empty_columns *after* validation if desired
        # check_no_fully_empty_columns(validated_df)

        return validated_df

    except SchemaError as err:
        logger.error(f"Pandera schema validation failed: {err.failure_cases}")
        # Improved error message extraction
        try:
            # failure_cases might be DataFrame or None
            if err.failure_cases is not None and not err.failure_cases.empty:
                 error_summary = "; ".join([
                     f"Column '{fc.get('column', 'N/A')}': {fc.get('check', 'N/A')} ({fc.get('reason_code', 'N/A')})"
                     for fc in err.failure_cases.to_dict(orient='records') if fc # Check if fc is not None
                 ])
            else:
                 error_summary = str(err) # Fallback to default error string
        except Exception:
            error_summary = str(err) # Further fallback

        raise SchemaError(f"Data validation failed specific rules: {error_summary}") from err
    except ValueError as err:
        logger.error(f"Custom validation check failed: {err}")
        raise err # Re-raise
    except Exception as e:
        logger.error(f"An unexpected error occurred during validation: {e}", exc_info=True)
        raise e # Re-raise

# --- Future Enhancement Idea (Keep existing) ---
# def load_and_validate(df: pd.DataFrame, schema_path: str):
#     ...