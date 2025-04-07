from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os
from src.config.settings import TARGET_URL, SELENIUM_HEADLESS
from src.core.portal import Portal
from dataclasses import dataclass

@dataclass
class Card:
    quantidade: str
    nome: str
    preco: str

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
            
        # Usar o perfil padrão do Chrome
        user_data_dir = os.path.expanduser('~') + '/AppData/Local/Google/Chrome/User Data'
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
        chrome_options.add_argument('--profile-directory=Default')
        
        # Configurações básicas para melhor compatibilidade
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver

    def _navigate_to_page(self):
        """Navigates to the target URL and waits for the page to load."""
        self.driver.get(TARGET_URL)
        self.logger.info("Page loaded successfully")
        time.sleep(2)  # Wait for initial page load

    def _get_credentials(self):
        """Retrieves login credentials from environment variables."""
        email = os.getenv('LIGAMAGIC_EMAIL')
        password = os.getenv('LIGAMAGIC_SENHA')
        
        if not email or not password:
            self.logger.error("Login credentials not found in .env file")
            return None, None
            
        # Add a space before the password
        password = " " + password
        return email, password

    def _find_dks_search_div(self):
        """Finds and returns the dks-search div element."""
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dks-search'))
        )

    def _extract_deck_titles(self, dks_search):
        """Extracts titles from all deckhome divs within the dks-search div."""
        deck_homes = dks_search.find_elements(By.CLASS_NAME, 'deckhome')
        deck_titles = []
        
        for deck in deck_homes:
            try:
                title = deck.get_attribute('title')
                if title and title.startswith('Pool'):
                    deck_titles.append(title)
                    self.logger.info(f"Found Pool deck: {title}")
            except Exception as e:
                self.logger.warning(f"Error extracting title from deck: {str(e)}")
                continue
                
        return deck_titles

    def _click_deck(self, deck):
        """Clicks on a specific deck."""
        try:
            self.logger.info(f"Clicando no deck: {deck.get_attribute('title')}")
            deck.click()
            time.sleep(5)  # Espera a página carregar
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao clicar no deck: {str(e)}")
            return False

    def _go_back(self):
        """Volta uma página no navegador."""
        try:
            self.driver.back()
            time.sleep(3)  # Espera a página carregar
            return True
        except Exception as e:
            self.logger.error(f"Erro ao voltar a página: {str(e)}")
            return False

    def login(self):
        """Performs login on the platform."""
        email, password = self._get_credentials()
        if not email or not password:
            return False
            
        return self.portal.login(email, password)
        
    def _extract_cards(self):
        """Extrai as informações das cartas do deck."""
        try:
            # Encontra o bloco principal do deck
            pdeck_block = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'pdeck-block'))
            )
            
            # Encontra todas as linhas do deck
            deck_lines = pdeck_block.find_elements(By.CLASS_NAME, 'deck-line')
            cards = []
            
            for line in deck_lines:
                try:
                    # Verifica se a linha tem todos os elementos necessários
                    qty = line.find_element(By.CLASS_NAME, 'deck-qty')
                    card = line.find_element(By.CLASS_NAME, 'deck-card')
                    price = line.find_element(By.CLASS_NAME, 'deck-price')
                    
                    # Cria um objeto Card com as informações
                    card_obj = Card(
                        quantidade=qty.text.strip(),
                        nome=card.text.strip(),
                        preco=price.text.strip()
                    )
                    
                    cards.append(card_obj)
                    self.logger.info(f"Card encontrado: {card_obj.quantidade}x {card_obj.nome} - {card_obj.preco}")
                    
                except Exception as e:
                    self.logger.warning(f"Erro ao extrair informações de uma linha: {str(e)}")
                    continue
            print(cards)
            return cards
            
        except Exception as e:
            self.logger.error(f"Erro ao extrair cartas: {str(e)}")
            return []

    def _extract_cards_from_deck(self, deck):
        """Extrai as cartas de um deck específico."""
        try:
            # Clica no deck
            if not self._click_deck(deck):
                self.logger.error("Não foi possível clicar no deck")
                return []
            
            # Extrai as cartas
            cards = self._extract_cards()
            
            # Volta para a página inicial
            self._navigate_to_page()
            time.sleep(5)  # Espera a página carregar
            
            return cards
            
        except Exception as e:
            self.logger.error(f"Erro ao extrair cartas do deck: {str(e)}")
            return []

    def scrape_data(self):
        """Performs data scraping from the LigaMagic website."""
        self.logger.info("Starting LigaMagic data scraping...")
        all_cards = []
        
        try:
            # Navigate to the page
            self._navigate_to_page()
            time.sleep(5)  # Wait for the page to load
            
            # Find the dks-search div and get all Pool decks
            dks_search = self._find_dks_search_div()
            deck_homes = dks_search.find_elements(By.CLASS_NAME, 'deckhome')
            
            # Armazena os títulos dos decks Pool
            pool_deck_titles = []
            for deck in deck_homes:
                title = deck.get_attribute('title')
                if title and title.startswith('Pool'):
                    pool_deck_titles.append(title)
            
            self.logger.info(f"Total de decks Pool encontrados: {len(pool_deck_titles)}")
            
            # Percorre todos os decks Pool pelos títulos
            for i, title in enumerate(pool_deck_titles, 1):
                try:
                    self.logger.info(f"Processando deck {i} de {len(pool_deck_titles)}: {title}")
                    
                    # Encontra o deck atual pelo título
                    dks_search = self._find_dks_search_div()
                    deck_homes = dks_search.find_elements(By.CLASS_NAME, 'deckhome')
                    current_deck = None
                    
                    for deck in deck_homes:
                        if deck.get_attribute('title') == title:
                            current_deck = deck
                            break
                    
                    if current_deck:
                        # Extrai as cartas do deck atual
                        cards = self._extract_cards_from_deck(current_deck)
                        all_cards.extend(cards)
                        self.logger.info(f"Total de cartas encontradas neste deck: {len(cards)}")
                        
                except Exception as e:
                    self.logger.error(f"Erro ao processar deck {i}: {str(e)}")
                    continue
            
            self.logger.info(f"Total de cartas encontradas em todos os decks: {len(all_cards)}")
            return all_cards
            
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")
            raise
            
        finally:
            self.driver.quit()
            
    def __del__(self):
        """Ensures the driver is closed when the instance is destroyed."""
        if hasattr(self, 'driver'):
            self.driver.quit() 