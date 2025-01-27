"""Main script for property scraping and processing."""
import logging
import sys
from typing import NoReturn
import os

from .web_scraper import get_all_property_details
from .property_parser import PropertyParser, AirtableManager
from .utils import ensure_directory_exists, setup_logging
from .config import scraper_config

def main() -> NoReturn:
    """Main execution function."""
    try:
        # Set up logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting property scraping process")
        
        # Ensure cache directory exists
        ensure_directory_exists(scraper_config.CACHE_DIR)
        
        try:
            # Initialize Airtable manager
            airtable_manager = AirtableManager()
            
            # Get property details
            logger.info("Fetching property details")
            html_contents = get_all_property_details()
            logger.info(f"Retrieved {len(html_contents)} property details pages")
            
            # Process each property
            success_count = 0
            error_count = 0
            
            for html_content in html_contents:
                try:
                    # Parse HTML content
                    details, status_history = PropertyParser.parse_html(html_content)
                    
                    # Create or update record
                    airtable_manager.create_or_update_record(details, status_history)
                    success_count += 1
                    
                except Exception as e:
                    logger.error(f"Failed to process property: {str(e)}")
                    error_count += 1
                    continue
            
            # Log summary
            logger.info("Property scraping process completed")
            logger.info(f"Successfully processed: {success_count} properties")
            if error_count > 0:
                logger.warning(f"Failed to process: {error_count} properties")
            
        except Exception as e:
            logger.error(f"Process failed: {str(e)}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()