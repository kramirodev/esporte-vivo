from fastapi import APIRouter, depends, HTTPException, status, Depends
from app.database import models
from app.database.schemas import UsuarioCreate, UsuarioResponse

router = APIRouter(
    prefix = '/user'
    tags = ['user']
)

@router.post('/', response_model = UsuarioCreate, status_code = status.HTTP_201_CREATED)
async def criar_usuario():


@router.get('/me', response_model = UsuarioResponse, status_code = status.HTTP_200_OK)
async def ler_usuario_atual(usuario_atual: models.Usuario = Depends(get_usuario_atual)):

    pass

@router.get('/me/inventario')
async def ler_inventario_usuario_atual():

    pass

@router.patch('/me/premium')
async def atualizar_premium_usuario_atual():

    pass