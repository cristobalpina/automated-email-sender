import pandas as pd
import logging
from typing import Optional


def load_excel_data(
    file_path: str, fill_value: str = "NO INFORMATION"
) -> Optional[pd.DataFrame]:
    """
    Loads data from an Excel file into a Pandas DataFrame.

    Args:
        file_path (str): Path to the Excel file.
        fill_value (str): Value to replace missing data (default: "NO INFORMATION").

    Returns:
        Optional[pd.DataFrame]: A Pandas DataFrame with the loaded data,
        or None if the file is not found or invalid.
    """
    try:
        # Attempt to load the Excel file
        data = pd.read_excel(file_path).fillna(fill_value)

        # Check if the DataFrame is empty
        if data.empty:
            logging.warning(
                f"The file '{file_path}' was loaded, but it contains no data."
            )
            return None

        # Log success and shape of the data
        logging.info(
            f"Successfully loaded Excel file '{file_path}' with {data.shape[0]} rows "
            f"and {data.shape[1]} columns."
        )
        return data

    except FileNotFoundError:
        logging.error(
            f"File '{file_path}' not found. Please check the path and try again."
        )
        return None
    except ValueError as e:
        logging.error(f"Invalid file format or content in '{file_path}': {e}")
        return None
    except Exception as e:
        logging.error(
            f"An unexpected error occurred while loading the Excel file '{file_path}': "
            f"{e}"
        )
        return None
