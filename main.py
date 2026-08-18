from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import schemas
from app.database.conexao import engine, get_db

app = FastAPI()

@app.post('/usuarios/', response_model=schemas.UsuarioResponse)
def criar_usuario(usuario_web: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    novo_usuario = 