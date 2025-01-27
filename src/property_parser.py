"""Property details parser and Airtable manager."""
from typing import Dict, List, Tuple, Optional
import logging
from bs4 import BeautifulSoup
import yaml
from pyairtable import Api

from .config import airtable_config, property_fields
from .utils import parse_monetary_value

logger = logging.getLogger(__name__)

class PropertyParser:
    """Handles parsing of property details from HTML content."""
    
    @staticmethod
    def parse_html(html_content: str) -> Tuple[Dict[str, str], List[Dict[str, str]]]:
        """
        Parse property details from HTML content.
        
        Args:
            html_content: HTML content to parse
            
        Returns:
            Tuple containing:
                - Dictionary of property details
                - List of status history dictionaries
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            details = PropertyParser._parse_details_table(soup)
            status_history = PropertyParser._parse_status_history(soup)
            return details, status_history
        except Exception as e:
            logger.error(f"Failed to parse HTML content: {str(e)}")
            raise
    
    @staticmethod
    def _parse_details_table(soup: BeautifulSoup) -> Dict[str, str]:
        """Parse the main details table."""
        details: Dict[str, str] = {}
        details_table = soup.find('table', class_='table-striped')
        
        if not details_table:
            logger.warning("Details table not found in HTML")
            return details
            
        try:
            for row in details_table.find_all('tr'):
                heading = row.find('td', class_='heading-bold columnwidth-15')
                value = row.find('td', class_=None)
                
                if heading and value:
                    key = heading.text.strip(":")
                    details[key] = value.text.strip()
                    
        except Exception as e:
            logger.error(f"Error parsing details table: {str(e)}")
            
        return details
    
    @staticmethod
    def _parse_status_history(soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Parse the status history table."""
        history: List[Dict[str, str]] = []
        status_table = soup.find('table', id='longTable')
        
        if not status_table:
            logger.warning("Status history table not found in HTML")
            return history
            
        try:
            for row in status_table.find_all('tr'):
                columns = row.find_all('td')
                if columns and len(columns) >= 2:
                    history.append({
                        'Status': columns[0].text.strip(),
                        'Date': columns[1].text.strip()
                    })
        except Exception as e:
            logger.error(f"Error parsing status history table: {str(e)}")
            
        return history

class AirtableManager:
    """Handles Airtable database operations."""
    
    def __init__(self):
        """Initialize Airtable API client."""
        if not airtable_config.API_KEY:
            raise ValueError("Airtable API key is required")
            
        self.api = Api(airtable_config.API_KEY)
        self.table = self.api.table(
            base_id=airtable_config.BASE_ID,
            table_name=airtable_config.TABLE_ID
        )
        self._existing_records: Optional[List[Dict]] = None
        
    @property
    def existing_records(self) -> List[Dict]:
        """Cached list of existing records."""
        if self._existing_records is None:
            self._existing_records = self.table.all()
        return self._existing_records
        
    def get_existing_sheriff_numbers(self) -> List[str]:
        """Get list of existing sheriff numbers."""
        return [
            record['fields']['Sheriff Number'] 
            for record in self.existing_records 
            if 'Sheriff Number' in record['fields']
        ]
        
    def create_or_update_record(
        self, 
        details: Dict[str, str], 
        status_history: List[Dict[str, str]]
    ) -> None:
        """
        Create or update a property record in Airtable.
        
        Args:
            details: Dictionary of property details
            status_history: List of status history dictionaries
        """
        try:
            sheriff_number = details[property_fields.SHERIFF_NUMBER]
            existing_numbers = self.get_existing_sheriff_numbers()
            
            record_data = self._prepare_record_data(details, status_history)
            
            if sheriff_number not in existing_numbers:
                self._create_record(sheriff_number, record_data)
            else:
                self._update_record(sheriff_number, record_data)
                
        except Exception as e:
            logger.error(f"Failed to create/update record: {str(e)}")
            raise
            
    def _prepare_record_data(
        self, 
        details: Dict[str, str], 
        status_history: List[Dict[str, str]]
    ) -> Dict:
        """Prepare record data for Airtable."""
        judgment_amount = parse_monetary_value(
            details.get(property_fields.JUDGMENT_AMOUNT)
        )
        good_faith_upset = parse_monetary_value(
            details.get(property_fields.GOOD_FAITH_UPSET)
        )
        
        return {
            "Sheriff Number": details[property_fields.SHERIFF_NUMBER],
            "Case Number": details.get(property_fields.CASE_NUMBER),
            "Address": details.get(property_fields.ADDRESS),
            "Sales Date": details.get(property_fields.SALES_DATE),
            "Plaintiff": details.get(property_fields.PLAINTIFF),
            "Defendant": details.get(property_fields.DEFENDANT),
            "Description": details.get(property_fields.DESCRIPTION),
            "Judgment Amount": judgment_amount if judgment_amount is not None else 0,
            "Good Faith Upset": good_faith_upset if good_faith_upset is not None else 0,
            "Attorney": details.get(property_fields.ATTORNEY),
            "Attorney Phone": details.get(property_fields.ATTORNEY_PHONE),
            "Status History": yaml.dump(status_history)
        }
        
    def _create_record(self, sheriff_number: str, record_data: Dict) -> None:
        """Create a new record in Airtable."""
        self.table.create(record_data)
        logger.info(f"Created record for sheriff number: {sheriff_number}")
        
    def _update_record(self, sheriff_number: str, record_data: Dict) -> None:
        """Update an existing record in Airtable."""
        for record in self.existing_records:
            if record["fields"].get("Sheriff Number") == sheriff_number:
                self.table.update(record["id"], record_data)
                logger.info(f"Updated record for sheriff number: {sheriff_number}")
                break