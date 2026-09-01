from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import models
from app.database.sqlalchemy_conexao import get_db
from app.database.schemas import EntrarFilaRequest, FilaResponse
from app.dependencies import get_current_user
from app.services.matchmaking import entrar_na_fila, sair_da_fila, consultar_status_usuario

router = APIRouter(
    prefix='/fila',
    tags=['Matchmaking - Fila']
)

@router.post('/entrar', status_code=status.HTTP_200_OK)
def entrar_fila(
    requisicao: EntrarFilaRequest,
    usuario_atual: models.usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    esporte_ids = list(dict.fromkeys(requisicao.esporte_ids))
    esportes = db.query(models.esporte).filter(
        models.esporte.id.in_(esporte_ids),
        models.esporte.ativo.is_(True)
    ).all()
    esportes_por_id = {esporte.id: esporte for esporte in esportes}
    inexistentes = [esporte_id for esporte_id in esporte_ids if esporte_id not in esportes_por_id]
    if inexistentes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Esportes inválidos ou inativos: {inexistentes}"
        )

    elos = db.query(models.usuario_elo).filter(
        models.usuario_elo.usuario_id == usuario_atual.id,
        models.usuario_elo.esporte_id.in_(esporte_ids)
    ).all()
    mmr_por_esporte = {elo.esporte_id: elo.pontuacao_elo for elo in elos}
    mmr_por_esporte.update({esporte_id: 1000 for esporte_id in esporte_ids if esporte_id not in mmr_por_esporte})

    resultado = entrar_na_fila(
        usuario_id=usuario_atual.id,
        esportes_ids=esporte_ids,
        mmr_por_esporte=mmr_por_esporte
    )

    if not resultado['sucesso']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado['motivo']
        )

    return {
        'mensagem': 'entrou na fila com sucesso.',
        'dados': resultado
    }

@router.delete('/sair', status_code=status.HTTP_200_OK)
def sair_fila(
    usuario_atual: models.usuario = Depends(get_current_user)
):
    resultado = sair_da_fila(usuario_id=usuario_atual.id)
    if not resultado['sucesso']:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=resultado['motivo']
        )
    return {
        'mensagem': 'removido da fila com sucesso'
    }

@router.get('/status', status_code=status.HTTP_200_OK)
def ver_status_fila(
    usuario_atual: models.usuario = Depends(get_current_user)
):
    return consultar_status_usuario(usuario_id=usuario_atual.id)