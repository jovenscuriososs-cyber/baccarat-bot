"""Cliente Firebase para armazenamento em tempo real"""

import asyncio
import json
from typing import List, Dict
from datetime import datetime
from loguru import logger
import aiohttp
from src.config.settings import settings

class FirebaseClient:
    """Cliente para Firebase Realtime Database"""
    
    def __init__(self):
        self.base_url = settings.FIREBASE_URL
        self.api_key = settings.FIREBASE_API_KEY
        self.history = []
    
    async def save_result(self, result: Dict):
        """Salvar resultado no Firebase"""
        try:
            url = f"{self.base_url}/bacbo/historico.json?auth={self.api_key}"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=result) as resp:
                    if resp.status in [200, 201]:
                        logger.debug(f"✅ Resultado salvo no Firebase: {result['resultado']}")
                        self.history.append(result)
                    else:
                        logger.error(f"Erro ao salvar no Firebase: {resp.status}")
        
        except Exception as e:
            logger.error(f"Erro ao salvar no Firebase: {e}")
    
    async def save_prediction(self, prediction: Dict):
        """Salvar previsão no Firebase"""
        try:
            prediction['timestamp'] = datetime.now().isoformat()
            url = f"{self.base_url}/bacbo/predicoes.json?auth={self.api_key}"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=prediction) as resp:
                    if resp.status in [200, 201]:
                        logger.debug(f"✅ Previsão salva: {prediction['outcome']} ({prediction['confidence']:.2%})")
                    else:
                        logger.error(f"Erro ao salvar previsão: {resp.status}")
        
        except Exception as e:
            logger.error(f"Erro ao salvar previsão: {e}")
    
    async def get_history(self, limit: int = 100) -> List[Dict]:
        """Obter histórico do Firebase"""
        try:
            url = f"{self.base_url}/bacbo/historico.json?auth={self.api_key}&limitToLast={limit}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if isinstance(data, dict):
                            return list(data.values())
                        return []
                    else:
                        logger.warning(f"Erro ao buscar histórico: {resp.status}")
                        return []
        
        except Exception as e:
            logger.error(f"Erro ao buscar histórico: {e}")
            return []
