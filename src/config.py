"""Configuration settings for the property scraper system."""
from typing import Final
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class AirtableConfig:
    """Airtable configuration settings."""
    API_KEY: Final[str] = os.getenv("AIRTABLE_API_KEY", "")
    BASE_ID: Final[str] = "appBbpDBlH7vjRYF3"
    TABLE_ID: Final[str] = "tblhFcS1EPGZNi5di"

@dataclass
class ScraperConfig:
    """Web scraper configuration settings."""
    BASE_URL: Final[str] = "https://salesweb.civilview.com"
    SEARCH_URL: Final[str] = f"{BASE_URL}/Sales/SalesSearch?countyId=10"
    CACHE_DIR: Final[str] = "property_details_cache"
    CACHE_EXPIRY: Final[int] = 24 * 60 * 60  # 24 hours in seconds
    WAIT_TIMEOUT: Final[int] = 10  # seconds to wait for elements

@dataclass
class HTMLSelectors:
    """HTML selectors for web scraping."""
    CITY_DROPDOWN: Final[str] = "CityDesc"
    SEARCH_BUTTON: Final[str] = "btn-primary"
    RESULTS_TABLE: Final[str] = "table-striped"
    DETAILS_LINK_TEXT: Final[str] = "Details"
    
@dataclass
class PropertyFields:
    """Property field mappings."""
    SHERIFF_NUMBER: Final[str] = "Sheriff #"
    CASE_NUMBER: Final[str] = "Court Case #"
    ADDRESS: Final[str] = "Address"
    SALES_DATE: Final[str] = "Sales Date"
    PLAINTIFF: Final[str] = "Plaintiff"
    DEFENDANT: Final[str] = "Defendant"
    DESCRIPTION: Final[str] = "Description"
    JUDGMENT_AMOUNT: Final[str] = "Judgment"
    GOOD_FAITH_UPSET: Final[str] = "Good Faith Upset*"
    ATTORNEY: Final[str] = "Attorney"
    ATTORNEY_PHONE: Final[str] = "Attorney Phone"

# Global instances
airtable_config = AirtableConfig()
scraper_config = ScraperConfig()
html_selectors = HTMLSelectors()
property_fields = PropertyFields()

# Validate required environment variables
if not airtable_config.API_KEY:
    raise ValueError("AIRTABLE_API_KEY environment variable is required")