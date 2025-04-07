from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
import logging
import time
from typing import Optional

class Portal:
    """Classe responsável por interagir com o portal LigaMagic."""
    
    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger: logging.Logger = logging.getLogger(__name__)
        
    def login(self, email: str, password: str) -> bool:
        """Realiza o login no portal."""
        try:
            self.logger.info("Starting login process...")
            
            # Wait for the login button to appear and click it
            login_button: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="dropdownMenuLogin"]/div'))
            )
            login_button.click()
            self.logger.info("Login modal opened")
            
            # Wait for the login modal to appear
            time.sleep(2)  # Small pause to ensure the modal is visible
            
            # Fill in the email
            email_field: WebElement = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="header-lnick"]'))
            )
            email_field.send_keys(email)
            
            # Fill in the password
            password_field: WebElement = self.driver.find_element(By.XPATH, '//*[@id="header-lsenha"]')
            password_field.send_keys(password)
            
            # Click the specified link
            login_link: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main-header"]/nav[1]/div/div[2]/div/div/div[1]/div/div[2]/form/div/ul/li[1]/a'))
            )
            login_link.click()
            self.logger.info("Login link clicked")
            
            # Wait 5 seconds
            time.sleep(5)
            self.logger.info("5-second wait completed")
            
            # Check if login was successful
            try:
                # Check if the login element is still present (login failed)
                login_elements: list[WebElement] = self.driver.find_elements(By.XPATH, '//*[@id="dropdownMenuLogin"]/div')
                if login_elements:
                    self.logger.error("Login failed - Invalid credentials or process error")
                    return False
                else:
                    self.logger.info("Login successful!")
                    return True
                    
            except Exception as e:
                self.logger.error(f"Error checking login status: {str(e)}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during login process: {str(e)}")
            return False

    def navigate_to_decks(self) -> bool:
        """Navega para a página de decks."""
        try:
            decks_link: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Decks"))
            )
            decks_link.click()
            
            # Aguarda a página de decks carregar
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "deck-list"))
            )
            
            self.logger.info("Successfully navigated to decks page")
            return True
            
        except Exception as e:
            self.logger.error(f"Error navigating to decks: {str(e)}")
            return False
    
    def get_deck_elements(self) -> list:
        """Retorna a lista de elementos de decks."""
        try:
            deck_elements: list[WebElement] = self.driver.find_elements(By.CLASS_NAME, "deck-item")
            self.logger.info(f"Found {len(deck_elements)} deck elements")
            return deck_elements
            
        except Exception as e:
            self.logger.error(f"Error getting deck elements: {str(e)}")
            return []
    
    def click_deck(self, deck_element) -> bool:
        """Clica em um deck específico."""
        try:
            deck_element.click()
            # Aguarda a página do deck carregar
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "deck-details"))
            )
            self.logger.info("Successfully clicked on deck")
            return True
            
        except Exception as e:
            self.logger.error(f"Error clicking on deck: {str(e)}")
            return False
    
    def go_back(self) -> bool:
        """Volta para a página anterior."""
        try:
            self.driver.back()
            # Aguarda a página anterior carregar
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "deck-list"))
            )
            self.logger.info("Successfully went back to deck list")
            return True
            
        except Exception as e:
            self.logger.error(f"Error going back: {str(e)}")
            return False
