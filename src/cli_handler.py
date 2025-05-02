# src/cli_handler.py
# Handles Command-Line Interface interactions

import pandas as pd


def get_model_choice() -> str | None:
    """Prompts the user to select a synthesizer model."""
    print("\\n--- Selecting Model ---")
    print("Choose a synthetic model:")
    print("1. GaussianCopula")
    print("2. CTGAN")
    print("3. TVAE")
    model_type = None
    while model_type not in ['GaussianCopula', 'CTGAN', 'TVAE']:
        model_choice = input("Select Model of choice (1, 2, or 3): ").strip()
        if model_choice == "1":
            model_type = "GaussianCopula"
        elif model_choice == "2":
            model_type = "CTGAN"
        elif model_choice == "3":
            model_type = "TVAE"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    print(f"Selected model: {model_type}")
    return model_type

def get_num_rows(default_rows: int) -> int:
    """Prompts the user for the number of synthetic rows to generate."""
    print("\\n--- Defining Synthetic Data Size ---")
    num_rows = default_rows
    try:
        user_input = input(
            f"How many synthetic rows do you want to generate? "
            f"(Press Enter to mimic original file size: {default_rows}): "
        ).strip()
        # Use default if input is empty, otherwise convert to int
        num_rows = int(user_input) if user_input else default_rows
        if num_rows <= 0:
            print("Number of rows must be positive. Using default.")
            num_rows = default_rows
    except ValueError:
        print("Invalid input. Using default number of rows.")
        num_rows = default_rows
    print(f"Will generate {num_rows} rows.")
    return num_rows


def get_columns_to_hash(synthetic_data_columns: pd.Index) -> list[str]:
    """Asks the user if they want to hash columns and which ones."""
    print("\\n--- Applying Privacy Hashing (Optional) ---")
    pii_columns_to_hash = []
    hash_choice = input("Do you want to hash any columns for privacy? (yes/no): ").strip().lower()

    if hash_choice == 'yes':
        print("Available columns in synthetic data:")
        for i, col in enumerate(synthetic_data_columns, 1):
            print(f"{i}. {col}")

        while True:
            try:
                input_str = input(
                    "Enter the numbers of the columns to hash (comma-separated, e.g., 1,3,5), "
                    "or press Enter to skip: "
                ).strip()
                if not input_str:
                    print("Skipping hashing.")
                    break
                # Convert input numbers (1-based index) to 0-based indices
                selected_indices = [int(x.strip()) - 1 for x in input_str.split(",")]
                # Validate indices and get column names
                pii_columns_to_hash = [
                    synthetic_data_columns[i] for i in selected_indices
                    if 0 <= i < len(synthetic_data_columns)
                ]
                if not pii_columns_to_hash:
                     print("No valid columns selected. Please try again or press Enter to skip.")
                     # Continue loop if selection was invalid but input was given
                else:
                     print(f"Selected columns for hashing: {pii_columns_to_hash}")
                     break # Exit loop after valid selection or skipping
            except (ValueError, IndexError) as e:
                print(f"Invalid input. Please enter comma-separated numbers corresponding "
                      f"to the columns. Error: {e}")
                # Continue loop on error

    else:
        print("Skipping hashing.")

    return pii_columns_to_hash