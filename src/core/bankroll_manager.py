"""Gerenciador de bankroll e apostas"""

from typing import List
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger

@dataclass
class BetRecord:
    """Registro de uma aposta"""
    amount: float
    result: str  # "WIN" ou "LOSS"
    timestamp: datetime
    round_number: int

class BankrollManager:
    """Gerencia bankroll, apostas e profitabilidade"""
    
    def __init__(self, initial_balance: float):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.bets: List[BetRecord] = []
        self.total_bets = 0
        self.wins = 0
        self.losses = 0
    
    def add_win(self, amount: float):
        """Adicionar vitória"""
        self.current_balance += amount
        self.wins += 1
        self.total_bets += 1
        self.bets.append(BetRecord(
            amount=amount,
            result="WIN",
            timestamp=datetime.now(),
            round_number=self.total_bets
        ))
    
    def add_loss(self, amount: float):
        """Adicionar derrota"""
        self.current_balance -= amount
        self.losses += 1
        self.total_bets += 1
        self.bets.append(BetRecord(
            amount=amount,
            result="LOSS",
            timestamp=datetime.now(),
            round_number=self.total_bets
        ))
    
    def get_win_rate(self) -> float:
        """Calcular taxa de vitória"""
        if self.total_bets == 0:
            return 0.0
        return self.wins / self.total_bets
    
    def get_profit(self) -> float:
        """Calcular lucro total"""
        return self.current_balance - self.initial_balance
    
    def get_roi(self) -> float:
        """Calcular ROI"""
        if self.initial_balance == 0:
            return 0.0
        return (self.get_profit() / self.initial_balance) * 100
    
    def get_statistics(self) -> dict:
        """Obter estatísticas completas"""
        return {
            "initial_balance": self.initial_balance,
            "current_balance": self.current_balance,
            "total_profit": self.get_profit(),
            "roi": self.get_roi(),
            "win_rate": self.get_win_rate(),
            "total_bets": self.total_bets,
            "wins": self.wins,
            "losses": self.losses,
            "avg_bet": sum(b.amount for b in self.bets) / len(self.bets) if self.bets else 0
        }
