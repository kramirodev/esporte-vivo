from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import manager

router = APIRouter(tags=['WebSockets'])


@router.websocket('/ws/fila/{usuario_id}')
async def websocket_fila(websocket: WebSocket, usuario_id: UUID):
    usuario = str(usuario_id)
    await manager.connect(usuario, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(usuario, websocket)
    except Exception:
        manager.disconnect(usuario, websocket)
