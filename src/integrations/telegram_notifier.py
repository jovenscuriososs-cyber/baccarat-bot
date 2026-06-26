"""Notificador via Telegram (stub)"""

from loguru import logger

class TelegramNotifier:
    """Notificador via Telegram"""
    
    def __init__(self):
        self.enabled = False
        logger.info("Telegram notifier desativado")
    
    async def send_message(self, message: str):
        """Enviar mensagem"""
        logger.debug(f"Telegram: {message}")
    
    async def send_alert(self, title: str, message: str):
        """Enviar alerta"""
        full_message = f"🚨 {title}\n{message}"
        await self.send_message(full_message)
