from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

# Allow imports from project root
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.config import Config
from etl.logger import get_logger

logger = get_logger(__name__)

class DatabaseConnector:
    """
    Manages database connections using SQLAlchemy.
    Implements Connection Pooling to efficiently handle multiple ETL requests 
    without overwhelming the database server.
    """
    def __init__(self):
        try:
            self.db_url = Config.get_db_url()
            
            # Initialize SQLAlchemy engine with production-grade pooling parameters
            self.engine = create_engine(
                self.db_url,
                pool_size=10,          # Maintain 10 connections in the pool
                max_overflow=20,       # Allow up to 20 temporary extra connections during bursts
                pool_timeout=30,       # Wait up to 30 seconds for a connection to be available
                pool_recycle=1800      # Recycle connections after 30 mins to avoid stale drops
            )
            
            # Session factory for transaction management
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.info("Database engine with connection pooling initialized successfully.")
            
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {e}")
            raise

    def get_engine(self):
        """Returns the SQLAlchemy engine."""
        return self.engine
        
    def get_session(self):
        """Returns a new SQLAlchemy session for database transactions."""
        return self.SessionLocal()
