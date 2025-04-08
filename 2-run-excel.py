from src.core.excel_handler import ExcelHandler
import logging

def setup_logging() -> None:
    """Configura o logging da aplicação."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main() -> None:
    """Função principal para atualizar o Excel com os dados do JSON."""
    try:
        # Configura o logging
        setup_logging()
        
        # Inicializa o ExcelHandler
        handler: ExcelHandler = ExcelHandler()
        
        # Lê o arquivo JSON
        data: dict = handler.read_json_file()
        
        # Atualiza o Excel
        excel_path: str = handler.update_excel(data)
        
        logging.info(f"Excel file updated successfully at: {excel_path}")
        
    except Exception as e:
        logging.error(f"Error during Excel update: {str(e)}")
        raise

if __name__ == "__main__":
    main() 