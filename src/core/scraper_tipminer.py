"""Scraper para TipMiner - Extrai resultados em tempo real"""

import asyncio
import aiohttp
from typing import List, Dict
from datetime import datetime
from loguru import logger
from bs4 import BeautifulSoup
from src.config.settings import settings

class TipMinerScraper:
    """Scraper do TipMiner para baccarat"""
    
    def __init__(self):
        self.url = settings.TIPMINER_URL
        self.last_results = []
        self.session = None
    
    async def fetch_results(self) -> List[Dict]:
        """Buscar resultados do TipMiner"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                async with session.get(self.url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        results = self._parse_html(html)
                        return results
                    else:
                        logger.warning(f"Status {resp.status} ao acessar TipMiner")
                        return []
        
        except asyncio.TimeoutError:
            logger.error("Timeout ao acessar TipMiner")
            return []
        except Exception as e:
            logger.error(f"Erro ao fazer scraping: {e}")
            return []
    
    def _parse_html(self, html: str) -> List[Dict]:
        """Parse do HTML do TipMiner"""
        results = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Procurar por elementos que contenham resultados
            # Ajuste os seletores conforme necessário para o site
            
            # Exemplo: procurar por divs com classes específicas
            result_elements = soup.find_all('div', class_='result')
            
            for elem in result_elements:
                try:
                    # Extrair dados do elemento
                    time_text = elem.find('span', class_='time')
                    number_text = elem.find('span', class_='number')
                    result_text = elem.find('span', class_='outcome')
                    
                    if time_text and number_text and result_text:
                        result = {
                            'horario': time_text.text.strip(),
                            'numero': int(number_text.text.strip()),
                            'resultado': result_text.text.strip().upper(),  # B, P, T
                            'timestamp': datetime.now().isoformat(),
                            'fonte': 'TipMiner'
                        }
                        results.append(result)
                except Exception as e:
                    logger.debug(f"Erro ao parsear elemento: {e}")
                    continue
            
            # Filtrar resultados novos
            new_results = [r for r in results if r not in self.last_results]
            self.last_results = results[-100:]  # Manter últimos 100
            
            return new_results
        
        except Exception as e:
            logger.error(f"Erro ao fazer parse HTML: {e}")
            return []
