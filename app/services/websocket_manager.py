from collections import defaultdict
from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, usuario_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[usuario_id].add(websocket)

    def disconnect(self, usuario_id: str, websocket: WebSocket):
        self.connections[usuario_id].discard(websocket)
        if not self.connections[usuario_id]:
            self.connections.pop(usuario_id, None)

    async def broadcast(self, usuarios: list[str], mensagem: dict):
        for usuario_id in usuarios:
            for websocket in list(self.connections.get(usuario_id, ())):
                try:
                    await websocket.send_json(mensagem)
                except Exception:
                    self.disconnect(usuario_id, websocket)


manager = WebSocketManager()
