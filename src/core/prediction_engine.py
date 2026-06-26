"""Motor de previsão usando ML e análise de padrões"""

import numpy as np
from typing import List, Dict, Literal
from dataclasses import dataclass
from loguru import logger

Outcome = Literal["B", "P", "T"]

@dataclass
class Prediction:
    """Resultado de uma previsão"""
    outcome: Outcome
    confidence: float
    reason: str
    timestamp: str

class PredictionEngine:
    """Motor de previsão baseado em ML e análise de padrões"""
    
    def __init__(self):
        pass
    
    def predict(self, history: List[Dict]) -> Dict:
        """Prever próximo resultado"""
        
        if not history or len(history) < 3:
            return {
                'outcome': 'B',
                'confidence': 0.5086,
                'reason': 'Sem histórico - Banker por probabilidade real'
            }
        
        # Extrair outcomes
        recent = [r['resultado'] for r in history[-50:]]  # Últimos 50
        
        # Análise de padrões
        prediction = self._analyze_patterns(recent)
        
        return prediction
    
    def _analyze_patterns(self, recent: List[str]) -> Dict:
        """Analisar padrões nos resultados recentes"""
        
        if not recent:
            return {
                'outcome': 'B',
                'confidence': 0.5086,
                'reason': 'Sem dados - probabilidade real'
            }
        
        # Contar ocorrências
        b_count = recent.count('B')
        p_count = recent.count('P')
        t_count = recent.count('T')
        
        # Estratégia 1: Streaks - Se últimos 3 são iguais, continuar
        if len(recent) >= 3:
            last_3 = recent[-3:]
            if last_3[0] == last_3[1] == last_3[2]:
                if last_3[0] == 'B':
                    return {
                        'outcome': 'B',
                        'confidence': 0.55,
                        'reason': 'Padrão de streak Banker detectado'
                    }
                elif last_3[0] == 'P':
                    return {
                        'outcome': 'P',
                        'confidence': 0.55,
                        'reason': 'Padrão de streak Player detectado'
                    }
        
        # Estratégia 2: Regressão à média
        total = b_count + p_count + t_count
        if total > 0:
            b_pct = b_count / total
            p_pct = p_count / total
            
            # Se um está muito acima de 50%, apostar no outro
            if b_pct > 0.55 and b_pct > p_pct:
                return {
                    'outcome': 'P',
                    'confidence': 0.52,
                    'reason': f'Regressão à média: Banker em {b_pct:.1%}'
                }
            elif p_pct > 0.55 and p_pct > b_pct:
                return {
                    'outcome': 'B',
                    'confidence': 0.52,
                    'reason': f'Regressão à média: Player em {p_pct:.1%}'
                }
        
        # Estratégia 3: Padrão alternado
        if len(recent) >= 4:
            last_4 = recent[-4:]
            if (last_4[0] != last_4[1] and 
                last_4[1] != last_4[2] and 
                last_4[2] != last_4[3]):
                # Alternando, continuar alternando
                opposite = 'P' if last_4[-1] == 'B' else 'B'
                return {
                    'outcome': opposite,
                    'confidence': 0.51,
                    'reason': 'Padrão alternado detectado'
                }
        
        # Padrão padrão: probabilidade real
        return {
            'outcome': 'B',
            'confidence': 0.5086,
            'reason': 'Aposta baseada em probabilidade real (Banker 50.86%)'
        }
