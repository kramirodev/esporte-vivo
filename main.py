import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routers.user import router as usuario_router
from app.routers.esportes import router as esporte_router
from app.routers.locais import router as local_router
from app.routers.disponibilidade import router as disponibilidade_router
from app.routers.partidas import router as partidas_router
from app.routers.fila import router as matchmaking_router
from app.routers.websocket import router as websocket_router
from app.services.matchmaking_worker import executar_worker

@asynccontextmanager
async def lifespan(app: FastAPI):
	stop_event = asyncio.Event()
	worker_task = asyncio.create_task(executar_worker(stop_event))
	try:
		yield
	finally:
		stop_event.set()
		await worker_task


app = FastAPI(lifespan=lifespan)

app.include_router(usuario_router)
app.include_router(esporte_router)
app.include_router(local_router)
app.include_router(disponibilidade_router)
app.include_router(partidas_router)
app.include_router(matchmaking_router)
app.include_router(websocket_router)