from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import models
from app.database.conexao import get_db
from app.database.schemas import DisponibilidadePadraoCreate, DisponibilidadePadraoResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix='/disponibilidade',
    tags=['disponibilidade']
)

@router.post('/me/disponibilidade', status_code=status.HTTP_201_CREATED)
def criar_disponibilidade(
    disp_web: DisponibilidadePadraoCreate,
    usuario_atual: models.usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Converte a coordenada (ela se aplica a todos os horários desse envio)
    ponto_wkt = f"POINT({disp_web.longitude} {disp_web.latitude})"
    geometria = func.ST_GeomFromText(ponto_wkt, 4326)

    novas_janelas = []
    
    # 2. Faz um loop pela lista de objetos de horário
    for janela in disp_web.horarios:
        
        nova_disponibilidade = models.disponibilidade_padrao(
            usuario_id=usuario_atual.id, 
            esporte_id=disp_web.esporte_id,
            dia_semana=janela.dia_semana,      
            hora_inicio=janela.hora_inicio,    
            hora_fim=janela.hora_fim,          
            geom_localizacao=geometria,
            raio_busca_km=disp_web.raio_busca_km
        )
        novas_janelas.append(nova_disponibilidade)

    if novas_janelas:
        db.add_all(novas_janelas)
        db.commit()
    
    return {"message": f"{len(novas_janelas)} janela(s) de disponibilidade cadastrada(s)!"}


@router.get('/me/disponibilidade', response_model=list[DisponibilidadePadraoResponse], status_code=status.HTTP_200_OK)
def ler_disponibilidade_usuario(
    usuario_atual: models.usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    disponibilidades = db.query(models.disponibilidade_padrao).filter(
        models.disponibilidade_padrao.usuario_id == usuario_atual.id
    ).all()
    
    return disponibilidades