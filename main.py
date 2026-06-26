#!/usr/bin/env python3
"""
Bot de Baccarat Completo - Entry Point Principal
Scraping TipMiner + Firebase + WhatsApp
"""

import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

from src.core.bot_manager import BotManager
from src.config.settings import settings
from src.utils.logger_setup import setup_logging

# Carregar variáveis de ambiente
load_dotenv()

# Setup logging
setup_logging()

async def main():
    """Função principal de execução"""
    logger.info("🎰 Iniciando Bot de Baccarat Completo...")
    logger.info(f"Modo: {settings.BOT_MODE}")
    logger.info(f"Bankroll Inicial: ${settings.STARTING_BANKROLL}")
    logger.info(f"Firebase: {settings.FIREBASE_URL}")
    logger.info(f"TipMiner Scrape: {settings.TIPMINER_SCRAPE_INTERVAL}s")
    
    try:
        # Inicializar gerenciador do bot
        bot = BotManager()
        
        # Iniciar bot
        await bot.start()
        
    except KeyboardInterrupt:
        logger.warning("\n🛑 Interrupção do usuário detectada")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot encerrado.")
