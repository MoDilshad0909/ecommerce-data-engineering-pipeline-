import pandas as pd
from pathlib import Path
import sys
from sqlalchemy.exc import SQLAlchemyError

# Allow imports from project root
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.database import DatabaseConnector
from etl.logger import get_logger

logger = get_logger(__name__)

def load_data_to_postgres(processed_dir: Path, db_connector: DatabaseConnector) -> None:
    """
    Loads all processed CSV files into the PostgreSQL database.
    Implements Transactions, Bulk Inserts, and automatic Rollback on failure.
    
    Args:
        processed_dir (Path): The directory containing cleaned CSV files.
        db_connector (DatabaseConnector): Initialized database connector instance.
    """
    if not processed_dir.exists():
        logger.error(f"Processed data directory does not exist: {processed_dir}")
        return

    csv_files = list(processed_dir.glob("*.csv"))
    if not csv_files:
        logger.warning(f"No CSV files found in {processed_dir} to load.")
        return

    engine = db_connector.get_engine()
    
    # Mapping raw CSV filenames to our target PostgreSQL Star Schema tables
    table_mapping = {
        'olist_customers_dataset.csv': 'dim_customers',
        'olist_products_dataset.csv': 'dim_products',
        'olist_sellers_dataset.csv': 'dim_sellers',
        'olist_orders_dataset.csv': 'dim_orders', 
        'olist_order_items_dataset.csv': 'fact_order_items',
        'olist_order_payments_dataset.csv': 'fact_payments'
    }

    for file_path in csv_files:
        filename = file_path.name
        table_name = table_mapping.get(filename)
        
        if not table_name:
            logger.info(f"Skipping {filename}: Not mapped to a target table.")
            continue
            
        logger.info(f"Loading {filename} into table '{table_name}'...")
        
        try:
            # Read the cleaned CSV
            df = pd.read_csv(file_path)
            
            # engine.begin() provides a Transaction block.
            # If an exception is raised inside the block, it automatically rolls back.
            # If successful, it automatically commits.
            with engine.begin() as connection:
                logger.info(f"Initiating bulk insert of {len(df)} rows to {table_name}...")
                
                # df.to_sql implements optimized bulk loading
                df.to_sql(
                    name=table_name,
                    con=connection,
                    if_exists='replace',  # Using replace for initial load. Use 'append' in incremental ETL.
                    index=False,
                    method='multi',       # Bulk insert via multiple VALUES clauses
                    chunksize=10000       # Prevent RAM exhaustion on large datasets
                )
            
            logger.info(f"Successfully loaded {filename} into '{table_name}'. Transaction committed.")
            
        except SQLAlchemyError as e:
            # SQLAlchemy connection automatically rolled back the transaction here
            logger.error(f"Database error while loading {filename}. Transaction rolled back.")
            logger.error(f"SQLAlchemyError Details: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading {filename}: {e}")

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent.parent
    processed_directory = project_root / 'data' / 'processed'
    
    logger.info("=== Starting Data Load Layer ===")
    
    try:
        db = DatabaseConnector()
        load_data_to_postgres(processed_directory, db)
    except Exception as e:
        logger.error(f"Critical failure in Data Load Layer: {e}")
        
    logger.info("=== Data Load Layer Execution Completed ===")
