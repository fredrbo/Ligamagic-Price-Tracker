import os
from dotenv import load_dotenv
from src.core.scraper import Scraper
from src.core.excel_handler import ExcelHandler
from src.utils.helpers import setup_logging

def main():
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Configura logging
    logger = setup_logging()
    logger.info("Iniciando o RPA...")
    
    try:
        # Inicializa o scraper
        scraper = Scraper()
        
        # Realiza a raspagem de dados
        data = scraper.scrape_data()
        
        # Exporta para Excel
        excel_handler = ExcelHandler()
        # excel_handler.export_to_excel(data)
        
        logger.info("Processo concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        raise

if __name__ == "__main__":
    main() 