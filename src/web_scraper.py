"""Web scraping module for property details."""
from typing import List, Optional
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from .config import scraper_config, html_selectors
from .utils import ensure_directory_exists

logger = logging.getLogger(__name__)

class PropertyScraper:
    """Handles web scraping of property details from Civil View website."""
    
    def __init__(self):
        """Initialize the PropertyScraper with Chrome WebDriver."""
        self.options = Options()
        self.options.add_argument('--headless')
        self.driver: Optional[webdriver.Chrome] = None
        ensure_directory_exists(scraper_config.CACHE_DIR)
        
    def __enter__(self):
        """Context manager entry point."""
        self.start_driver()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        self.close_driver()
        
    def start_driver(self):
        """Initialize and start the Chrome WebDriver."""
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=self.options
            )
            logger.info("Chrome WebDriver started successfully")
        except WebDriverException as e:
            logger.error(f"Failed to start Chrome WebDriver: {str(e)}")
            raise
            
    def close_driver(self):
        """Safely close the WebDriver."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Chrome WebDriver closed")
            
    def wait_for_element(self, by: By, value: str, timeout: Optional[int] = None) -> None:
        """
        Wait for an element to be present on the page.
        
        Args:
            by: Selenium By locator strategy
            value: Locator value
            timeout: Optional custom timeout in seconds
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized")
            
        timeout = timeout or scraper_config.WAIT_TIMEOUT
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException as e:
            logger.error(f"Timeout waiting for element {value}: {str(e)}")
            raise
            
    def get_property_details(self) -> List[str]:
        """
        Retrieve property details HTML from Civil View website.
        
        Returns:
            List of HTML content for each property details page
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized")
            
        try:
            # Navigate to search page
            self.driver.get(scraper_config.SEARCH_URL)
            
            # Select Jersey City from dropdown
            self.wait_for_element(By.NAME, html_selectors.CITY_DROPDOWN)
            city_dropdown = Select(self.driver.find_element(By.NAME, html_selectors.CITY_DROPDOWN))
            city_dropdown.select_by_visible_text('JERSEY CITY')
            
            # Click search button
            search_button = self.driver.find_element(By.CLASS_NAME, html_selectors.SEARCH_BUTTON)
            search_button.click()
            
            # Wait for results
            self.wait_for_element(By.CLASS_NAME, html_selectors.RESULTS_TABLE)
            
            # Get all detail links
            detail_links = [
                link.get_attribute('href') 
                for link in self.driver.find_elements(By.LINK_TEXT, html_selectors.DETAILS_LINK_TEXT)
            ]
            
            property_details = []
            for href in detail_links:
                property_id = href.split("=")[-1]
                cache_file = f"{scraper_config.CACHE_DIR}/{property_id}.html"
                
                # Check cache first
                if self._is_cache_valid(cache_file):
                    content = self._read_from_cache(cache_file)
                    if content:
                        property_details.append(content)
                        continue
                
                # Fetch and cache if needed
                content = self._fetch_and_cache_details(href, cache_file)
                if content:
                    property_details.append(content)
                    
            return property_details
            
        except Exception as e:
            logger.error(f"Error fetching property details: {str(e)}")
            raise
            
    def _is_cache_valid(self, cache_file: str) -> bool:
        """Check if cached file exists and is not expired."""
        import os
        if not os.path.exists(cache_file):
            return False
        return time.time() - os.path.getmtime(cache_file) < scraper_config.CACHE_EXPIRY
        
    def _read_from_cache(self, cache_file: str) -> Optional[str]:
        """Read HTML content from cache file."""
        try:
            with open(cache_file, 'r', encoding='utf-8') as file:
                content = file.read()
                logger.info(f"Read HTML from cache: {cache_file}")
                return content
        except Exception as e:
            logger.warning(f"Failed to read cache file {cache_file}: {str(e)}")
            return None
            
    def _fetch_and_cache_details(self, href: str, cache_file: str) -> Optional[str]:
        """Fetch property details and cache the result."""
        if not self.driver:
            raise RuntimeError("WebDriver not initialized")
            
        try:
            self.driver.get(href)
            self.wait_for_element(By.CLASS_NAME, html_selectors.RESULTS_TABLE)
            content = self.driver.page_source
            
            # Cache the content
            with open(cache_file, 'w', encoding='utf-8') as file:
                file.write(content)
                logger.info(f"Cached HTML to: {cache_file}")
            
            return content
            
        except Exception as e:
            logger.error(f"Failed to fetch/cache details from {href}: {str(e)}")
            return None

def get_all_property_details() -> List[str]:
    """
    Convenience function to get all property details.
    
    Returns:
        List of HTML content for each property details page
    """
    with PropertyScraper() as scraper:
        return scraper.get_property_details()