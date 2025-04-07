import pandas as pd
import logging
from src.config.settings import OUTPUT_DIR, EXCEL_OUTPUT_FILENAME

class ExcelHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.output_file = f"{OUTPUT_DIR}/{EXCEL_OUTPUT_FILENAME}"
        
    def export_to_excel(self, data):
        """Exporta os dados para um arquivo Excel."""
        self.logger.info("Iniciando exportação para Excel...")
        
        try:
            # Converte os dados para DataFrame
            df = pd.DataFrame(data)
            
            # Exporta para Excel
            df.to_excel(self.output_file, index=False)
            
            self.logger.info(f"Dados exportados com sucesso para: {self.output_file}")
            
        except Exception as e:
            self.logger.error(f"Erro durante a exportação para Excel: {str(e)}")
            raise 