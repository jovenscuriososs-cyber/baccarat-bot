"""Gerenciador principal do bot"""

import asyncio
from loguru import logger
from src.config.settings import settings
from src.core.scraper_tipminer import TipMinerScraper
from src.core.prediction_engine import PredictionEngine
from src.core.bankroll_manager import BankrollManager
from src.integrations.firebase_client import FirebaseClient
from src.integrations.greenapi_client import GreenAPIClient

class BotManager:
    """Gerenciador central do bot de baccarat"""
    
    def __init__(self):
        self.mode = settings.BOT_MODE
        self.bankroll_manager = BankrollManager(settings.STARTING_BANKROLL)
        self.scraper = TipMinerScraper()
        self.prediction_engine = PredictionEngine()
        self.firebase = FirebaseClient()
        self.whatsapp = GreenAPIClient() if settings.GREENAPI_ENABLED else None
        self.running = False
        
    async def start(self):
        """Iniciar o bot"""
        self.running = True
        logger.info(f"🚀 Bot iniciado em modo: {self.mode}")
        
        try:
            # Iniciar tarefas assíncronas
            await asyncio.gather(
                self._scrape_tipminer_loop(),
                self._prediction_loop(),
            )
        except KeyboardInterrupt:
            logger.warning("Interrupção detectada")
        finally:
            self.running = False
            await self.shutdown()
    
    async def _scrape_tipminer_loop(self):
        """Loop contínuo de scraping do TipMiner"""
        logger.info("📡 Iniciando scraping do TipMiner...")
        
        while self.running:
            try:
                # Scraping
                results = await self.scraper.fetch_results()
                
                if results:
                    logger.success(f"✅ {len(results)} resultados obtidos")
                    
                    # Salvar no Firebase
                    for result in results:
                        await self.firebase.save_result(result)
                        logger.info(f"📊 {result['resultado']} - #{result['numero']}")
                
                await asyncio.sleep(settings.TIPMINER_SCRAPE_INTERVAL)
                
            except Exception as e:
                logger.error(f"Erro no scraping: {e}")
                await asyncio.sleep(5)
    
    async def _prediction_loop(self):
        """Loop contínuo de previsões"""
        logger.info("🔮 Iniciando engine de previsões...")
        
        while self.running:
            try:
                # Obter histórico do Firebase
                history = await self.firebase.get_history()
                
                if len(history) > 5:
                    # Fazer previsão
                    prediction = self.prediction_engine.predict(history)
                    logger.info(f"🎯 Previsão: {prediction['outcome']} (confiança: {prediction['confidence']:.2%})")
                    
                    # Salvar previsão
                    await self.firebase.save_prediction(prediction)
                    
                    # Enviar notificação WhatsApp
                    if self.whatsapp:
                        message = f"🎰 Previsão Baccarat: {prediction['outcome']}\nConfiança: {prediction['confidence']:.2%}\nMotivo: {prediction['reason']}"
                        await self.whatsapp.send_message(message)
                
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"Erro na previsão: {e}")
                await asyncio.sleep(5)
    
    async def shutdown(self):
        """Desligar o bot"""
        logger.info("🛑 Encerrando bot...")
        
        # Mostrar resumo final
        final_balance = self.bankroll_manager.current_balance
        total_profit = final_balance - self.bankroll_manager.initial_balance
        
        logger.info(f"\n📊 RESUMO FINAL:")
        logger.info(f"   Bankroll Inicial: ${self.bankroll_manager.initial_balance}")
        logger.info(f"   Bankroll Final: ${final_balance}")
        logger.info(f"   Lucro/Prejuízo: ${total_profit}")
        logger.info(f"   Taxa de Vitória: {self.bankroll_manager.get_win_rate():.2%}")
