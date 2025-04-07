from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

class Portal:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        
    def login(self, email, password):
        """Performs login on the LigaMagic platform."""
        try:
            self.logger.info("Starting login process...")
            
            
            # Wait for the login button to appear and click it
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="dropdownMenuLogin"]/div'))
            )
            login_button.click()
            self.logger.info("Login modal opened")
            
            # Wait for the login modal to appear
            time.sleep(2)  # Small pause to ensure the modal is visible
            
            # Fill in the email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="header-lnick"]'))
            )
            email_field.send_keys(email)
            
            # Fill in the password
            password_field = self.driver.find_element(By.XPATH, '//*[@id="header-lsenha"]')
            password_field.send_keys(password)
            
            # Click the specified link
            login_link = WebDriverWait(self.driver, 10).until(
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
                if self.driver.find_elements(By.XPATH, '//*[@id="dropdownMenuLogin"]/div'):
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
