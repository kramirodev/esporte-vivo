from fastapi import FastAPI
from app.routers.user import router as usuario_router
from app.routers.esportes import router as esporte_router
from app.routers.locais import router as local_router
from app.routers.disponibilidade import router as disponibilidade_router
from app.routers.partidas import router as partidas_router
from app.routers.fila import router as matchmaking_router
from app.routers.websocket import router as websocket_router


app = FastAPI(title="Esporte Vivo API")

app.include_router(usuario_router)
app.include_router(esporte_router)
app.include_router(local_router)
app.include_router(disponibilidade_router)
app.include_router(partidas_router)
app.include_router(matchmaking_router)
app.include_router(websocket_router)