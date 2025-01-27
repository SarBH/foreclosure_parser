"""Utility functions for the property scraper system."""
from typing import Optional
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('property_scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def parse_monetary_value(value: Optional[str]) -> Optional[float]:
    """
    Parse a monetary value string into a float.
    
    Args:
        value: String containing monetary value (e.g., "$1,234.56")
        
    Returns:
        Float value if parsing successful, None if value is None or parsing fails
        
    Example:
        >>> parse_monetary_value("$1,234.56")
        1234.56
        >>> parse_monetary_value(None)
        None
    """
    if not value:
        return None
        
    try:
        # Remove currency symbol and commas, then convert to float
        cleaned_value = value.strip("$").replace(",", "")
        return float(cleaned_value)
    except (ValueError, AttributeError) as e:
        logger.warning(f"Failed to parse monetary value '{value}': {str(e)}")
        return None

def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to the directory to check/create
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory_path}")
    except Exception as e:
        logger.error(f"Failed to create directory {directory_path}: {str(e)}")
        raise

def setup_logging(log_file: str = 'property_scraper.log') -> None:
    """
    Set up logging configuration.
    
    Args:
        log_file: Path to the log file
    """
    try:
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir:
            ensure_directory_exists(log_dir)
            
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        logger.info("Logging configured successfully")
    except Exception as e:
        print(f"Failed to configure logging: {str(e)}")
        raise