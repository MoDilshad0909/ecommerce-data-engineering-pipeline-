import pandas as pd
from pathlib import Path
from typing import Dict
import sys

# Add project root to sys.path so we can run this file directly from VS Code
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from etl.logger import get_logger

logger = get_logger(__name__)

def extract_datasets(raw_data_dir: Path) -> Dict[str, pd.DataFrame]:
    """
    Reads all CSV files from the raw data directory, extracts them using Pandas,
    logs their metadata (rows, cols, memory usage), and handles exceptions.
    
    Args:
        raw_data_dir (Path): The directory containing raw CSV files.
        
    Returns:
        Dict[str, pd.DataFrame]: A dictionary where keys are filenames and values are DataFrames.
    """
    datasets: Dict[str, pd.DataFrame] = {}
    
    if not raw_data_dir.exists():
        logger.error(f"Raw data directory does not exist: {raw_data_dir}")
        return datasets

    # Automatically detect all CSV files
    csv_files = list(raw_data_dir.glob("*.csv"))
    
    if not csv_files:
        logger.warning(f"No CSV files found in {raw_data_dir}")
        return datasets
        
    logger.info(f"Found {len(csv_files)} CSV files to extract.")

    for file_path in csv_files:
        filename = file_path.name
        
        # Check if it is a valid file
        if not file_path.is_file():
            logger.warning(f"{filename} is not a valid file. Skipping.")
            continue
            
        try:
            logger.info(f"Extracting {filename}...")
            # Read using pandas, explicit utf-8 encoding for safety
            df = pd.read_csv(file_path, encoding='utf-8')
            
            # Display dataset stats
            rows, columns = df.shape
            memory_usage_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
            
            logger.info(f"Successfully extracted {filename}:")
            logger.info(f" - Rows: {rows}")
            logger.info(f" - Columns: {columns}")
            logger.info(f" - Memory Usage: {memory_usage_mb:.2f} MB")
            
            # Store inside dictionary
            datasets[filename] = df
            
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error while reading {filename}: {e}")
        except pd.errors.EmptyDataError:
            logger.error(f"File {filename} is completely empty.")
        except Exception as e:
            logger.error(f"An unexpected error occurred while reading {filename}: {e}")
            
    return datasets

if __name__ == "__main__":
    # Test the extraction logic
    raw_dir = project_root / 'data' / 'raw'
    logger.info("=== Starting Data Extraction Layer ===")
    extracted_data = extract_datasets(raw_dir)
    logger.info(f"=== Extraction Complete: {len(extracted_data)} files loaded ===")
