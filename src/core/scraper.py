from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Optional, Tuple
import time
import logging
import os
import json
from datetime import datetime
from src.config.settings import TARGET_URL, SELENIUM_HEADLESS
from src.core.portal import Portal
from dataclasses import dataclass, asdict

@dataclass
class Card:
    quantity: str
    name: str
    price: str

class Scraper:
    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.driver: WebDriver = self._setup_driver()
        self.portal: Portal = Portal(self.driver)
        
    def _setup_driver(self) -> WebDriver:
        """Configures and returns a WebDriver instance."""
        chrome_options: Options = Options()
        if SELENIUM_HEADLESS:
            chrome_options.add_argument('--headless')
            
        # Usar o perfil padrão do Chrome
        user_data_dir: str = os.path.expanduser('~') + '/AppData/Local/Google/Chrome/User Data'
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
        chrome_options.add_argument('--profile-directory=Default')
        
        # Configurações básicas para melhor compatibilidade
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        
        service: Service = Service(ChromeDriverManager().install())
        driver: WebDriver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver

    def _navigate_to_page(self) -> None:
        """Navigates to the target URL and waits for the page to load."""
        self.driver.get(TARGET_URL)
        self.logger.info("Page loaded successfully")
        time.sleep(2)  # Wait for initial page load

    def _get_credentials(self) -> Tuple[Optional[str], Optional[str]]:
        """Retrieves login credentials from environment variables."""
        email: Optional[str] = os.getenv('LIGAMAGIC_EMAIL')
        password: Optional[str] = os.getenv('LIGAMAGIC_SENHA')
        
        if not email or not password:
            self.logger.error("Login credentials not found in .env file")
            return None, None
            
        # Add a space before the password
        password = " " + password
        return email, password

    def _find_dks_search_div(self) -> WebElement:
        """Finds and returns the dks-search div element."""
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dks-search'))
        )

    def _extract_deck_titles(self, dks_search: WebElement) -> List[str]:
        """Extracts titles from all deckhome divs within the dks-search div."""
        deck_homes: List[WebElement] = dks_search.find_elements(By.CLASS_NAME, 'deckhome')
        deck_titles: List[str] = []

        for deck in deck_homes:
            try:
                title: Optional[str] = deck.get_attribute('title')
                if title and title.startswith('Pool'):
                    deck_titles.append(title)
                    self.logger.info(f"Found Pool deck: {title}")
            except Exception as e:
                self.logger.warning(f"Error extracting title from deck: {str(e)}")
                continue
                
        return deck_titles

    def _click_deck(self, deck: WebElement) -> bool:
        """Clicks on a specific deck."""
        try:
            # Encontra a div picture dentro do deckhome
            picture_div: WebElement = deck.find_element(By.CLASS_NAME, 'picture')
            self.logger.info(f"Clicking on deck: {deck.get_attribute('title')}")
            picture_div.click()
            time.sleep(5)  # Espera a página carregar
            return True
            
        except Exception as e:
            self.logger.error(f"Error clicking on deck: {str(e)}")
            return False

    def _go_back(self) -> bool:
        """Volta uma página no navegador."""
        try:
            self.driver.back()
            time.sleep(3)  # Espera a página carregar
            return True
        except Exception as e:
            self.logger.error(f"Error going back: {str(e)}")
            return False

    def login(self) -> bool:
        """Performs login on the platform."""
        email: Optional[str]
        password: Optional[str]
        email, password = self._get_credentials()
        if not email or not password:
            return False
            
        return self.portal.login(email, password)
        
    def _extract_cards(self) -> List[Card]:
        """Extrai as informações das cartas do deck."""
        try:
            # Encontra o bloco principal do deck
            pdeck_block: WebElement = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'pdeck-block'))
            )
            
            # Encontra todas as linhas do deck
            deck_lines: List[WebElement] = pdeck_block.find_elements(By.CLASS_NAME, 'deck-line')
            cards: List[Card] = []
            
            for line in deck_lines:
                try:
                    # Verifica se a linha tem todos os elementos necessários
                    qty: WebElement = line.find_element(By.CLASS_NAME, 'deck-qty')
                    card: WebElement = line.find_element(By.CLASS_NAME, 'deck-card')
                    price: WebElement = line.find_element(By.CLASS_NAME, 'deck-price')
                    
                    # Cria um objeto Card com as informações
                    card_obj: Card = Card(
                        quantity=qty.text.strip(),
                        name=card.text.strip(),
                        price=price.text.strip()
                    )
                    
                    cards.append(card_obj)
                    self.logger.info(f"Card found: {card_obj.quantity}x {card_obj.name} - {card_obj.price}")
                    
                except Exception as e:
                    self.logger.warning(f"Error extracting card information: {str(e)}")
                    continue
            print(cards)
            return cards
            
        except Exception as e:
            self.logger.error(f"Error extracting cards: {str(e)}")
            return []

    def _extract_cards_from_deck(self, deck: WebElement) -> List[Card]:
        """Extrai as cartas de um deck específico."""
        try:
            # Clica no deck
            if not self._click_deck(deck):
                self.logger.error("Could not click on deck")
                return []
            
            # Extrai as cartas
            cards: List[Card] = self._extract_cards()
            
            # Volta para a página inicial
            self._navigate_to_page()
            time.sleep(5)  # Espera a página carregar
            
            return cards
            
        except Exception as e:
            self.logger.error(f"Error extracting cards from deck: {str(e)}")
            return []

    def save_cards_to_json(self, cards: List[Card], filename: str = "cards.json") -> None:
        """Salva os cards em um arquivo JSON com a data da extração."""
        try:
            # Cria o diretório de saída se não existir
            output_dir: str = "output"
            os.makedirs(output_dir, exist_ok=True)
            
            # Cria o caminho completo do arquivo
            filepath: str = os.path.join(output_dir, filename)
            
            # Prepara os dados para salvar
            data: dict = {
                "extraction_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_cards": len(cards),
                "cards": [asdict(card) for card in cards]
            }
            
            # Salva os dados em JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            self.logger.info(f"Cards saved successfully in: {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving cards to JSON: {str(e)}")
            raise

    def scrape_data(self) -> List[Card]:
        """Performs data scraping from the LigaMagic website."""
        self.logger.info("Starting LigaMagic data scraping...")
        all_cards: List[Card] = []
        
        try:
            # Navigate to the page
            self._navigate_to_page()
            time.sleep(5)  # Wait for the page to load
            
            # Find the dks-search div and get all Pool decks
            dks_search: WebElement = self._find_dks_search_div()
            deck_homes: List[WebElement] = dks_search.find_elements(By.CLASS_NAME, 'deckhome')
            
            # Armazena os títulos dos decks Pool
            pool_deck_titles: List[str] = []
            for deck in deck_homes:
                title: Optional[str] = deck.get_attribute('title')
                if title and title.startswith('Pool'):
                    pool_deck_titles.append(title)
            
            self.logger.info(f"Total Pool decks found: {len(pool_deck_titles)}")
            
            # Percorre todos os decks Pool pelos títulos
            for i, title in enumerate(pool_deck_titles, 1):
                try:
                    self.logger.info(f"Processing deck {i} of {len(pool_deck_titles)}: {title}")
                    
                    # Encontra o deck atual pelo título
                    dks_search = self._find_dks_search_div()
                    deck_homes = dks_search.find_elements(By.CLASS_NAME, 'deckhome')
                    current_deck: Optional[WebElement] = None
                    
                    for deck in deck_homes:
                        if deck.get_attribute('title') == title:
                            current_deck = deck
                            break
                    
                    if current_deck:
                        # Extrai as cartas do deck atual
                        cards: List[Card] = self._extract_cards_from_deck(current_deck)
                        all_cards.extend(cards)
                        self.logger.info(f"Total cards found in this deck: {len(cards)}")
                        
                except Exception as e:
                    self.logger.error(f"Error processing deck {i}: {str(e)}")
                    continue
            
            self.logger.info(f"Total cards found in all decks: {len(all_cards)}")
            
            # Salva os cards em JSON
            self.save_cards_to_json(all_cards)
            
            return all_cards
            
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")
            raise
            
        finally:
            self.driver.quit()
            
    def __del__(self) -> None:
        """Ensures the driver is closed when the instance is destroyed."""
        if hasattr(self, 'driver'):
            self.driver.quit() 