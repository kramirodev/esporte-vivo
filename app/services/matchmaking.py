from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import models
from datetime import datetime

def buscar_jogadores_compativeis(db: Session, local: models.local_partida, esporte_id: int):
    agora = datetime.now()
    dia_atual = agora.weekday()
    hora_atual = agora.time()

    jogadores = db.query(
        models.disponibilidade_padrao.usuario_id,
        models.usuario_elo.pontuacao_elo
    ).join(
        models.usuario_elo,
        (models.usuario_elo.usuario_id == models.disponibilidade_padrao.usuario_id) &
        (models.usuario_elo.esporte_id == esporte_id)
    ).filter(
        models.disponibilidade_padrao.esporte_id == esporte_id,
        models.disponibilidade_padrao.dia_semana == dia_atual,
        models.disponibilidade_padrao.hora_inicio <= hora_atual,
        models.disponibilidade_padrao.hora_fim >= hora_atual,

        func.ST_DWithin(
            func.Geography(models.disponibilidade_padrao.geom_localizacao),
            func.Geography(local.geom_localizacao),
            models.disponibilidade_padrao.raio_busca_km * 1000
            )
    ).order_by(
        models.usuario_elo.pontuacao_elo.desc()
    ).all()

    return jogadores