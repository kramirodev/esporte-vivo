from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import models
from app.database.conexao import get_db
from app.database.schemas import UsuarioCreate, UsuarioResponse, InventarioUsuarioResponse, EsporteResponse, VincularEsportesRequest
from app.dependencies import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/', response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario_web: UsuarioCreate, db: Session = Depends(get_db)):

    usuario_existente = db.query(models.usuario).filter(models.usuario.telefone == usuario_web.telefone).first()
    if usuario_existente: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário com este telefone já existe.",
        )

    dados_usuario = usuario_web.model_dump(exclude={'latitude', 'longitude'})

    if usuario_web.latitude is not None and usuario_web.longitude is not None:
        ponto_wkt = f"POINT({usuario_web.longitude} {usuario_web.latitude})"
        dados_usuario['geom_localizacao'] = func.ST_GeomFromText(ponto_wkt, 4326)

    novo_usuario = models.usuario(**dados_usuario)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get('/me', response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
def ler_usuario_atual(usuario_atual: models.usuario = Depends(get_current_user)):
    return usuario_atual

@router.get('/me/inventario', response_model=list[InventarioUsuarioResponse], status_code=status.HTTP_200_OK)
def ler_inventario_usuario_atual(
    usuario_atual: models.usuario = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    inventario = db.query(models.inventario_usuario).filter(
        models.inventario_usuario.usuario_id == usuario_atual.id
    ).all()
    
    return inventario

@router.patch('/me/premium')
def atualizar_premium_usuario_atual():
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)

@router.post('/me/esportes', status_code=status.HTTP_201_CREATED)
def definir_esportes_do_usuario(
    requisicao: VincularEsportesRequest,
    usuario_atual: models.usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    novos_elos = []
    
    for esporte_id in requisicao.esporte_ids:
        existe = db.query(models.usuario_elo).filter(
            models.usuario_elo.usuario_id == usuario_atual.id,
            models.usuario_elo.esporte_id == esporte_id
        ).first()

        if not existe:
            novo_elo = models.usuario_elo(
                usuario_id=usuario_atual.id,
                esporte_id=esporte_id,
                pontuacao_elo=0,
                partidas_jogadas=0,
                vitorias=0,
                derrotas=0
            )
            novos_elos.append(novo_elo)

    if novos_elos:
        db.add_all(novos_elos)
        db.commit()

    return {"message": "Esportes definidos com sucesso."}
