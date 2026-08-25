from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import models
from datetime import datetime

def buscar_jogadores_compativeis(db: Session, local: models.local_partida, esporte_id: int):
    