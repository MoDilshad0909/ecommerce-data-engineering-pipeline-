import logging
import os
from pathlib import Path

def get_logger(module_name: str) -> logging.Logger:
    """
    Creates and returns a reusable logger that writes to logs/app.log.
    
    Args:
        module_name (str): The name of the module generating the log (usually __name__).
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Define the log directory relative to the current file (etl/logger.py)
    # This ensures it finds the project root logs/ folder.
    project_root = Path(__file__).resolve().parent.parent
    log_dir = project_root / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / 'app.log'

    logger = logging.getLogger(module_name)
    
    # Avoid duplicate logs if the logger already has handlers
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Formatting: Timestamp - Module - Level - Message
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # File Handler: Appends to logs/app.log
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console Handler: Prints to the terminal
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
