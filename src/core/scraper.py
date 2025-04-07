from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import logging
import os
from src.config.settings import TARGET_URL, SELENIUM_HEADLESS
from src.core.portal import Portal

class Scraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = self._setup_driver()
        self.portal = Portal(self.driver)
        
    def _setup_driver(self):
        """Configures and returns a WebDriver instance."""
        chrome_options = Options()
        if SELENIUM_HEADLESS:
            chrome_options.add_argument('--headless')
            
        # Additional settings for better compatibility
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
        
    def login(self):
        """Performs login on the platform."""
        email = os.getenv('LIGAMAGIC_EMAIL')
        password = os.getenv('LIGAMAGIC_SENHA')
        
        if not email or not password:
            self.logger.error("Login credentials not found in .env file")
            return False
            
        return self.portal.login(email, password)
        
    def scrape_data(self):
        """Performs data scraping from the LigaMagic website."""
        self.logger.info("Starting LigaMagic data scraping...")
        
        try:
            # Access the initial page
            self.driver.get(TARGET_URL)
            self.logger.info("Page loaded successfully")
            
            # Perform login
            if not self.login():
                self.logger.error("Could not login. Aborting scraping.")
                return []
                
            # Wait for the page to load after login
            time.sleep(5)
            
            # Locate the decks table
            decks_table = self.driver.find_element(By.CLASS_NAME, 'decks')
            
            # Find all decks on the page
            decks = decks_table.find_elements(By.CLASS_NAME, 'deck')
            
            data = []
            for deck in decks:
                try:
                    # Extract deck information
                    deck_name = deck.find_element(By.CLASS_NAME, 'deck-name').text
                    deck_format = deck.find_element(By.CLASS_NAME, 'deck-format').text
                    deck_date = deck.find_element(By.CLASS_NAME, 'deck-date').text
                    
                    # Add data to the list
                    data.append({
                        'Deck Name': deck_name,
                        'Format': deck_format,
                        'Date': deck_date
                    })
                    
                    self.logger.info(f"Deck extracted: {deck_name}")
                    
                except Exception as e:
                    self.logger.warning(f"Error extracting deck information: {str(e)}")
                    continue
            
            self.logger.info(f"Total decks extracted: {len(data)}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")
            raise
            
        finally:
            self.driver.quit()
            
    def __del__(self):
        """Ensures the driver is closed when the instance is destroyed."""
        if hasattr(self, 'driver'):
            self.driver.quit() 