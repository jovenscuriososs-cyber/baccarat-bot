import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    """Configurações globais da aplicação"""
    
    # Modo de operação
    BOT_MODE: str = os.getenv("BOT_MODE", "simulation")
    
    # Firebase
    FIREBASE_URL: str = os.getenv("FIREBASE_URL", "")
    FIREBASE_API_KEY: str = os.getenv("FIREBASE_API_KEY", "")
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    
    # GreenAPI (WhatsApp)
    GREENAPI_URL: str = os.getenv("GREENAPI_URL", "")
    GREENAPI_INSTANCE_ID: str = os.getenv("GREENAPI_INSTANCE_ID", "")
    GREENAPI_TOKEN: str = os.getenv("GREENAPI_TOKEN", "")
    GREENAPI_ENABLED: bool = bool(os.getenv("GREENAPI_TOKEN"))
    
    # TipMiner
    TIPMINER_URL: str = os.getenv("TIPMINER_URL", "https://www.tipminer.com/br/historico/jonbet/bac-bo")
    TIPMINER_SCRAPE_INTERVAL: int = int(os.getenv("TIPMINER_SCRAPE_INTERVAL", 10))
    
    # Estratégia
    STARTING_BANKROLL: float = float(os.getenv("STARTING_BANKROLL", 1000))
    MIN_BET: float = float(os.getenv("MIN_BET", 10))
    MAX_BET: float = float(os.getenv("MAX_BET", 500))
    WIN_TARGET: float = float(os.getenv("WIN_TARGET", 500))
    LOSE_LIMIT: float = float(os.getenv("LOSE_LIMIT", -500))
    
    # Logging
    LOG_LEVEL: str = os.getenv("BOT_LOG_LEVEL", "INFO")
    LOG_FILE: str = "logs/bot.log"
    
    # Dashboard Web
    DASHBOARD_HOST: str = os.getenv("DASHBOARD_HOST", "0.0.0.0")
    DASHBOARD_PORT: int = int(os.getenv("DASHBOARD_PORT", 5000))
    DASHBOARD_DEBUG: bool = os.getenv("DASHBOARD_DEBUG", "False").lower() == "true"
    
    # WhatsApp Notifications
    WHATSAPP_NOTIFY: bool = os.getenv("WHATSAPP_NOTIFY", "True").lower() == "true"
    WHATSAPP_NUMBERS: list = os.getenv("WHATSAPP_NUMBERS", "").split(",") if os.getenv("WHATSAPP_NUMBERS") else []
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///baccarat.db")
    
    def __post_init__(self):
        """Validar configurações"""
        if self.BOT_MODE not in ["simulation", "live"]:
            raise ValueError(f"BOT_MODE deve ser 'simulation' ou 'live', recebido: {self.BOT_MODE}")
        
        if not self.FIREBASE_URL:
            raise ValueError("FIREBASE_URL não configurada")

# Instância global
settings = Settings()
