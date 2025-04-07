import os
import logging
from src.config.settings import LOG_FILE, LOG_FORMAT, LOG_LEVEL

def setup_logging():
    """Configura o sistema de logging do projeto."""
    # Cria o diretório de logs se não existir
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Configura o logger
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def create_directories():
    """Cria os diretórios necessários para o projeto."""
    directories = [
        'data/input',
        'data/output',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
def validate_environment():
    """Valida se todas as variáveis de ambiente necessárias estão configuradas."""
    required_vars = [
        'TARGET_URL'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(
            f"Variáveis de ambiente ausentes: {', '.join(missing_vars)}"
        ) 