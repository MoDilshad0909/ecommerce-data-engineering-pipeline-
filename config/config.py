import os
from pathlib import Path
from dotenv import load_dotenv

# Automatically load environment variables from the .env file in the config/ directory
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """
    Centralized configuration class that reads from environment variables.
    Fails early if critical database parameters are missing.
    """
    # Database Configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "ecommerce_dw")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

    @classmethod
    def get_db_url(cls) -> str:
        """
        Constructs and returns the SQLAlchemy database URL.
        """
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
