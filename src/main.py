from src.core.scraper import Scraper, Card
from typing import List
import logging

def setup_logging() -> None:
    """Configura o logging da aplicação."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main() -> None:
    """Função principal da aplicação."""
    try:
        # Configura o logging
        setup_logging()
        
        # Inicializa o scraper
        scraper: Scraper = Scraper()
        
        # Executa o scraping
        cards: List[Card] = scraper.scrape_data()
        
        # Exibe o total de cartas encontradas
        logging.info(f"Total de cartas encontradas: {len(cards)}")
        
    except Exception as e:
        logging.error(f"Erro durante a execução: {str(e)}")
        raise

if __name__ == "__main__":
    main() 