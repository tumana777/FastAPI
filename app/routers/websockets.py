from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws")

# @router.websocket("/chat")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"You said: {data.capitalize()}")

# class ConnectionManager:
#     def __init__(self):
#         self.connections = []
#
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.connections.append(websocket)
#
#     async def disconnect(self, websocket: WebSocket):
#         self.connections.remove(websocket)
#
#     async def broadcast(self, message: str):
#         for connection in self.connections:
#             await connection.send_text(message)
#
# manager = ConnectionManager()
#
# @router.websocket("/chat")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#
#             client = websocket.client
#
#             await manager.broadcast(f"User {client.host}:{client.port} said: {data}")
#     except WebSocketDisconnect:
#         await manager.disconnect(websocket)

class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.connections[websocket] = username

    def disconnect(self, websocket: WebSocket):
        self.connections.pop(websocket)

    async def broadcast(self, message: str):
        for websocket, username in self.connections.items():
            await websocket.send_text(f"{message}")

manager = ConnectionManager()


@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)

    await manager.broadcast(f"{username} has joined the chat")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")

    except WebSocketDisconnect:

        manager.disconnect(websocket)
        await manager.broadcast(f"{username} has left the chat")














