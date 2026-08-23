from fastapi import APIRouter, HTTPException, status, Depends, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.database.conexao import get_db
import app.database.models as models

router = APIRouter()

api_key_header = APIKeyHeader(name='X-API-KEY')

def get_current_user(
        api_key: str = Security(api_key_header),
        db: Session = Depends(get_db)):

    usuario = db.query(models.usuario).filter(models.usuario.api_key == api_key).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida",
        )

    return usuario

def get_is_admin(
        usuario_atual: models.usuario = Depends(get_current_user)):

    if not usuario_atual.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Usuário não é administrador.",
        )

    return usuario_atual