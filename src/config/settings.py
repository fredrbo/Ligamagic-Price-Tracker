import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
INPUT_DIR = os.path.join(DATA_DIR, 'input')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Configurações do Selenium
SELENIUM_DRIVER_PATH = os.getenv('SELENIUM_DRIVER_PATH', '')
SELENIUM_HEADLESS = os.getenv('SELENIUM_HEADLESS', 'False').lower() == 'true'

# Configurações do Excel
EXCEL_OUTPUT_FILENAME = os.getenv('EXCEL_OUTPUT_FILENAME', 'output.xlsx')

# Configurações de Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.path.join(LOGS_DIR, 'rpa.log')

# URLs e outros parâmetros específicos do scraping
TARGET_URL = os.getenv('TARGET_URL', '') 