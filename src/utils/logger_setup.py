"""Configuração de logging"""

from pathlib import Path
from loguru import logger
from src.config.settings import settings

def setup_logging():
    """Configurar sistema de logging"""
    
    # Criar diretório de logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Remover handler padrão
    logger.remove()
    
    # Adicionar handler para console
    logger.add(
        lambda msg: print(msg, end=""),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL
    )
    
    # Adicionar handler para arquivo
    logger.add(
        settings.LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="500 MB",
        retention="10 days"
    )
    
    logger.info("✅ Sistema de logging inicializado")
