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
    usuario_atual: models.usuario = Depends(get_current_user)
):
    resultado = entrar_na_fila(
        usuario_id=usuario_atual.id,
        esportes_ids=requisicao.esporte_ids  # <-- Corrigido: esportes_ids (plural)
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