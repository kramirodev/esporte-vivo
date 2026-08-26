from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import models
from datetime import datetime

def obter_peso_por_elo(pontuacao: int) -> float:
    if pontuacao >= 4000: return 1.00  # Challenger
    if pontuacao >= 3500: return 0.95  # Grandmaster
    if pontuacao >= 3000: return 0.90  # Master
    if pontuacao >= 2500: return 0.85  # Diamond
    if pontuacao >= 2000: return 0.80  # Platinum
    if pontuacao >= 1500: return 0.70  # Gold
    if pontuacao >= 1000: return 0.65  # Silver
    if pontuacao >= 500:  return 0.60  # Bronze
    return 0.55                        # Iron

def calcular_pontuacao_total(db: Session, jogador_id: int) -> int: 
    pontuacao_total = db.query()
