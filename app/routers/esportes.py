from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import models
from app.database.sqlalchemy_conexao import get_db
from app.database.schemas import EsporteResponse, EsporteCreate
from app.dependencies import get_is_admin

router = APIRouter(
    prefix='/esportes',
    tags=['esportes'])

@router.get('/', response_model=list[EsporteResponse], status_code=status.HTTP_200_OK)
def ler_esportes(db: Session = Depends(get_db)):
    esportes = db.query(models.esporte).all()
    return esportes

@router.post('/adicionar-esporte', response_model = EsporteCreate, status_code=status.HTTP_201_CREATED)
def adicionar_esporte(esporte_web: EsporteCreate, db: Session = Depends(get_db), admin: models.usuario = Depends(get_is_admin)):
    novo_esporte = models.esporte(**esporte_web.model_dump())
    db.add(novo_esporte)
    db.commit()
    db.refresh(novo_esporte)
    return novo_esporte
