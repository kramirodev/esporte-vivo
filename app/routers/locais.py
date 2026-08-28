from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import models
from app.database.sqlalchemy_conexao import get_db
from app.database.schemas import LocalPartidaResponse, LocalPartidaCreate
from app.dependencies import get_is_admin

router = APIRouter(
    prefix='/locais',
    tags=['locais'])

@router.get('/', response_model=list[LocalPartidaResponse], status_code=status.HTTP_200_OK)
def ler_locais(db: Session = Depends(get_db)):
    locais = db.query(models.local_partida).all()
    return locais

@router.post('/adicionar-local', status_code=status.HTTP_201_CREATED)
def adicionar_local(local_web: LocalPartidaCreate, db: Session = Depends(get_db), admin: models.usuario = Depends(get_is_admin)):

    ponto_wkt = f"POINT({local_web.longitude} {local_web.latitude})"

    geometria = func.ST_GeomFromText(ponto_wkt, 4326)

    novo_local = models.local_partida(
        nome = local_web.nome,
        tipo_local = local_web.tipo_local,
        geom_localizacao = geometria,
        endereco = local_web.endereco,
        valor_hora = local_web.valor_hora,
    )

    db.add(novo_local)
    db.commit()
    db.refresh(novo_local)
    return novo_local

