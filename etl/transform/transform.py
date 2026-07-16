import pandas as pd
from pathlib import Path
from typing import Dict
import sys

# Add project root to sys.path so we can run this file directly from VS Code
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from etl.logger import get_logger
from etl.utils import (
    to_snake_case, 
    generate_missing_value_report, 
    generate_duplicate_report, 
    convert_to_datetime, 
    save_csv
)
from etl.extract.extract import extract_datasets

logger = get_logger(__name__)

def validate_dataset(df: pd.DataFrame, filename: str) -> None:
    """
    Performs data validation before transformation and generates a report.
    
    Args:
        df (pd.DataFrame): The DataFrame to validate.
        filename (str): Name of the file for reporting purposes.
    """
    logger.info(f"--- Validation Report for {filename} ---")
    
    # 1. Empty file check
    if df.empty:
        logger.warning(f"Validation Warning: {filename} is empty!")
        return
        
    # 2. Shape
    rows, cols = df.shape
    logger.info(f"Shape: {rows} rows, {cols} columns")
    
    # 3. Duplicate row count
    duplicates = generate_duplicate_report(df)
    logger.info(f"Duplicate Rows: {duplicates}")
    
    # 4. Missing values count & Null percentage
    missing_report = generate_missing_value_report(df)
    total_cells = rows * cols
    total_missing = missing_report.sum()
    null_percentage = (total_missing / total_cells) * 100 if total_cells > 0 else 0
    
    logger.info(f"Total Missing Values: {total_missing}")
    logger.info(f"Overall Null Percentage: {null_percentage:.2f}%")
    
    # 5. Data type summary
    logger.info(f"Data Types:\n{df.dtypes.to_string()}")
    logger.info("-" * 40)

def transform_datasets(datasets: Dict[str, pd.DataFrame], processed_dir: Path) -> None:
    """
    Cleans and transforms a dictionary of DataFrames, then saves them to processed_dir.
    
    Args:
        datasets (Dict[str, pd.DataFrame]): Dictionary of extracted datasets.
        processed_dir (Path): Destination path for cleaned datasets.
    """
    if not datasets:
        logger.warning("No datasets provided for transformation.")
        return
        
    for filename, original_df in datasets.items():
        logger.info(f"Transforming {filename}...")
        
        # TASK 5: Keep original dataset unchanged
        df = original_df.copy()
        
        # TASK 4: Validate data before transformation
        validate_dataset(df, filename)
        
        # 1. Remove duplicate rows
        duplicates_before = generate_duplicate_report(df)
        if duplicates_before > 0:
            df = df.drop_duplicates()
            logger.info(f"Removed {duplicates_before} duplicate rows.")
            
        # 2. Rename columns to snake_case & Strip spaces
        df = to_snake_case(df)
        
        # 3. Handle missing values 
        # Here we drop entirely empty rows (invalid records)
        initial_rows = len(df)
        df = df.dropna(how='all') 
        
        # 4. Standardize text values & strip spaces in actual data
        str_cols = df.select_dtypes(include=['object']).columns
        for col in str_cols:
            # Lowercase and strip whitespace for string columns
            df[col] = df[col].astype(str).str.strip().str.lower()
            # Restore True Nulls instead of 'nan' strings
            df.loc[df[col] == 'nan', col] = None
            
        # 5. Convert dates
        # Auto-detect date columns based on naming convention
        date_cols = [col for col in df.columns if 'date' in col or 'timestamp' in col]
        if date_cols:
            df = convert_to_datetime(df, date_cols)
            logger.info(f"Converted columns to datetime: {date_cols}")
            
        # 6. Remove invalid records (e.g. completely null rows that we dropped)
        dropped_rows = initial_rows - len(df)
        if dropped_rows > 0:
            logger.info(f"Removed {dropped_rows} invalid/empty records.")
            
        # Save cleaned dataset
        save_path = processed_dir / filename
        save_csv(df, save_path)
        
if __name__ == "__main__":
    # Test the Extract and Transform process together
    raw_dir = project_root / 'data' / 'raw'
    processed_dir = project_root / 'data' / 'processed'
    
    logger.info("=== Starting ETL Pipeline (Extract & Transform) ===")
    
    # Extract Layer
    raw_datasets = extract_datasets(raw_dir)
    
    # Transform Layer
    transform_datasets(raw_datasets, processed_dir)
    
    logger.info("=== ETL Pipeline Execution Completed ===")
