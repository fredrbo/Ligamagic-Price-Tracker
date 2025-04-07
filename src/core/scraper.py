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
        """Configura e retorna uma instância do WebDriver."""
        chrome_options = Options()
        if SELENIUM_HEADLESS:
            chrome_options.add_argument('--headless')
            
        # Configurações adicionais para melhor compatibilidade
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
        
    def fazer_login(self):
        """Realiza o login na plataforma."""
        email = os.getenv('LIGAMAGIC_EMAIL')
        senha = os.getenv('LIGAMAGIC_SENHA')
        
        if not email or not senha:
            self.logger.error("Credenciais de login não encontradas no arquivo .env")
            return False
            
        return self.portal.fazer_login(email, senha)
        
    def scrape_data(self):
        """Realiza a raspagem de dados do site da LigaMagic."""
        self.logger.info("Iniciando raspagem de dados da LigaMagic...")
        
        try:
            # Acessa a página inicial
            self.driver.get(TARGET_URL)
            self.logger.info("Página carregada com sucesso")
            
            # Realiza o login
            if not self.fazer_login():
                self.logger.error("Não foi possível fazer login. Abortando raspagem.")
                return []
                
            # Aguarda o carregamento da página após o login
            time.sleep(5)
            
            # Localiza a tabela de decks
            decks_table = self.driver.find_element(By.CLASS_NAME, 'decks')
            
            # Encontra todos os decks na página
            decks = decks_table.find_elements(By.CLASS_NAME, 'deck')
            
            data = []
            for deck in decks:
                try:
                    # Extrai informações do deck
                    deck_name = deck.find_element(By.CLASS_NAME, 'deck-name').text
                    deck_format = deck.find_element(By.CLASS_NAME, 'deck-format').text
                    deck_date = deck.find_element(By.CLASS_NAME, 'deck-date').text
                    
                    # Adiciona os dados à lista
                    data.append({
                        'Nome do Deck': deck_name,
                        'Formato': deck_format,
                        'Data': deck_date
                    })
                    
                    self.logger.info(f"Deck extraído: {deck_name}")
                    
                except Exception as e:
                    self.logger.warning(f"Erro ao extrair informações de um deck: {str(e)}")
                    continue
            
            self.logger.info(f"Total de decks extraídos: {len(data)}")
            return data
            
        except Exception as e:
            self.logger.error(f"Erro durante a raspagem: {str(e)}")
            raise
            
        finally:
            self.driver.quit()
            
    def __del__(self):
        """Garante que o driver seja fechado ao destruir a instância."""
        if hasattr(self, 'driver'):
            self.driver.quit() 