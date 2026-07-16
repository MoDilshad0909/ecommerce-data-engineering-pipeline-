import pandas as pd
from pathlib import Path
from typing import List

from etl.logger import get_logger

logger = get_logger(__name__)

def to_snake_case(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts all column names in the DataFrame to snake_case.
    Strips leading/trailing spaces, replaces inner spaces with underscores,
    and converts to lowercase.
    
    Args:
        df (pd.DataFrame): The pandas DataFrame to modify.
        
    Returns:
        pd.DataFrame: DataFrame with snake_case columns.
    """
    df.columns = (df.columns
                  .str.strip()
                  .str.replace(' ', '_')
                  .str.lower())
    return df

def generate_missing_value_report(df: pd.DataFrame) -> pd.Series:
    """
    Calculates the count of missing (null) values for each column.
    
    Args:
        df (pd.DataFrame): The pandas DataFrame to analyze.
        
    Returns:
        pd.Series: Series containing null counts per column.
    """
    return df.isnull().sum()

def generate_duplicate_report(df: pd.DataFrame) -> int:
    """
    Calculates the total number of duplicate rows in the DataFrame.
    
    Args:
        df (pd.DataFrame): The pandas DataFrame to analyze.
        
    Returns:
        int: Total duplicate row count.
    """
    return int(df.duplicated().sum())

def convert_to_datetime(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Converts a list of specified columns in the DataFrame to datetime objects.
    Invalid dates will be coerced to NaT (Not a Time).
    
    Args:
        df (pd.DataFrame): The pandas DataFrame to modify.
        columns (List[str]): List of column names to convert.
        
    Returns:
        pd.DataFrame: DataFrame with updated datetime columns.
    """
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        else:
            logger.warning(f"Column '{col}' not found for datetime conversion.")
    return df

def save_csv(df: pd.DataFrame, file_path: Path) -> None:
    """
    Saves the DataFrame to a CSV file at the specified path.
    
    Args:
        df (pd.DataFrame): The pandas DataFrame to save.
        file_path (Path): The destination path for the CSV.
    """
    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=False)
        logger.info(f"Successfully saved file to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save file to {file_path}. Error: {e}")
        raise
