from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import jwt
from app.dependencies import SECRET_KEY
from app.db.models import UserInDB

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
)

# Manager to track active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[websocket] = client_id

    def disconnect(self, websocket: WebSocket):
        self.active_connections.pop(websocket, None)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message: {e}")

# JWT decoder to get the user
def decode_token(token: str) -> UserInDB:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if not username:
            raise ValueError("Username missing in token")
        return UserInDB(username=username)
    except jwt.PyJWTError as e:
        raise ValueError(f"Token decode error: {e}")

manager = ConnectionManager()

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    # Parse token from query param
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        print("Connection rejected: token not provided")
        return
    try:
        user = decode_token(token)
    except ValueError as e:
        await websocket.close(code=1008)
        print(f"Connection rejected: {e}")
        return

    await manager.connect(websocket, user.username)
    await manager.broadcast(f"++ {user.username} joined the chat ++")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{user.username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"-- {user.username} left the chat --")
    except Exception as e:
        print(f"Unexpected error: {e}")
        await websocket.close(code=1011)
