from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
)
class ConnectionManager:
      def __init__(self):
           self.active_connections: dict[WebSocket, str] = {}
      async def connect(self,websocket:WebSocket,client_id: str):
           await websocket.accept()
           self.active_connections[websocket] = client_id
      def disconnect(self,websocket:WebSocket):
            self.active_connections.pop(websocket,None)
      async def broadcast(self,message:str):
            for connection in self.active_connections:
                  await connection.send_text(message)

manager = ConnectionManager()
@router.websocket("/chat/{client_id}")
async def websocket_endpoint(websocket:WebSocket,client_id:str):
      await manager.connect(websocket,client_id)
      try:
            while True:
                  data = await websocket.receive_text()
                  await manager.broadcast(f"{client_id}:{data}")
      except WebSocketDisconnect:
            manager.disconnect(websocket)
            await manager.broadcast(f"-- {client_id}: Disconnected --")