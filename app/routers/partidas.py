from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import models
from app.database.conexao import get_db
from app.database.schemas import PartidaCreate, PartidaResponse, PartidaJogadorCreate
from app.dependencies import get_is_admin

router = APIRouter(
    prefix='/partidas',
    tags=['partidas']
)

@router.post('/', response_model=PartidaResponse, status_code=status.HTTP_201_CREATED)
def criar_partida_manualmente(
    partida_web: PartidaCreate, 
    db: Session = Depends(get_db), 
    admin: models.usuario = Depends(get_is_admin)
):
    """Rota para o sistema/admin criar o lobby da partida."""
    
    nova_partida = models.partida(
        esporte_id=partida_web.esporte_id,
        local_id=partida_web.local_id,
        tipo=partida_web.tipo,
        data_hora_agendada=partida_web.data_hora_agendada,
        status="agendada" 
    )
    
    db.add(nova_partida)
    db.commit()
    db.refresh(nova_partida)
    
    return nova_partida


@router.post('/jogadores', status_code=status.HTTP_201_CREATED)
def alocar_jogador_na_partida(
    alocacao_web: PartidaJogadorCreate,
    db: Session = Depends(get_db),
    admin: models.usuario = Depends(get_is_admin)
):
    """Rota para o sistema/admin alocar um usuário dentro de uma partida existente."""
    
    # Verifica se a partida existe
    partida_existe = db.query(models.partida).filter(models.partida.id == alocacao_web.partida_id).first()
    if not partida_existe:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
        
    # Verifica se o usuário já está nesta partida
    jogador_ja_alocado = db.query(models.partida_jogador).filter(
        models.partida_jogador.partida_id == alocacao_web.partida_id,
        models.partida_jogador.usuario_id == alocacao_web.usuario_id
    ).first()
    
    if jogador_ja_alocado:
        raise HTTPException(status_code=400, detail="Jogador já alocado nesta partida.")

    novo_jogador = models.partida_jogador(
        partida_id=alocacao_web.partida_id,
        usuario_id=alocacao_web.usuario_id,
        time_alocado=alocacao_web.time_alocado,
        compareceu=False, 
        variacao_elo_obtida=0
    )
    
    db.add(novo_jogador)
    db.commit()
    
    return {"message": f"Jogador alocado no {alocacao_web.time_alocado} com sucesso!"}