"""Cliente GreenAPI para notificações via WhatsApp"""

import asyncio
from typing import List
from loguru import logger
import aiohttp
from src.config.settings import settings

class GreenAPIClient:
    """Cliente para GreenAPI (WhatsApp)"""
    
    def __init__(self):
        self.instance_id = settings.GREENAPI_INSTANCE_ID
        self.token = settings.GREENAPI_TOKEN
        self.base_url = settings.GREENAPI_URL
        self.numbers = settings.WHATSAPP_NUMBERS
    
    async def send_message(self, message: str, phone_number: str = None):
        """Enviar mensagem via WhatsApp"""
        try:
            if not phone_number and not self.numbers:
                logger.warning("Nenhum número configurado para WhatsApp")
                return
            
            numbers = [phone_number] if phone_number else self.numbers
            
            for number in numbers:
                await self._send_to_number(message, number)
        
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem WhatsApp: {e}")
    
    async def _send_to_number(self, message: str, phone_number: str):
        """Enviar para um número específico"""
        try:
            # Formatar número
            chat_id = f"{phone_number}@c.us"
            
            url = f"{self.base_url}/waInstance{self.instance_id}/sendMessage/{self.token}"
            
            payload = {
                "chatId": chat_id,
                "message": message
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        logger.info(f"✅ Mensagem enviada para {phone_number}")
                    else:
                        logger.error(f"Erro ao enviar para {phone_number}: {resp.status}")
        
        except Exception as e:
            logger.error(f"Erro ao enviar para {phone_number}: {e}")
    
    async def send_alert(self, title: str, message: str):
        """Enviar alerta formatado"""
        full_message = f"🎰 {title}\n\n{message}"
        await self.send_message(full_message)
