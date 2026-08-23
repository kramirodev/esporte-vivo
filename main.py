from fastapi import FastAPI
from app.routers.user import router as usuario_router
from app.routers.esportes import router as esporte_router
from app.routers.locais import router as local_router
from app.routers.disponibilidade import router as disponibilidade_router
from app.routers.partidas import router as partidas_router

app = FastAPI()

app.include_router(usuario_router)
app.include_router(esporte_router)
app.include_router(local_router)
app.include_router(disponibilidade_router)
app.include_router(partidas_router)