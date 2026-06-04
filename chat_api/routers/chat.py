from fastapi import APIRouter, WebSocket , Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import asyncio

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket): #when someone connects , accept there inviatoin
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket): #when someone disconnects , reject there invitation
        self.active_connections.remove(websocket) 

    async def broadcast(self, message: str): #loop through every connectinog and send them the msg
      await asyncio.gather(
        *[connection.send_text(message) for connection in self.active_connections]
    )

manager = ConnectionManager()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


from fastapi import WebSocketDisconnect

@router.websocket("/chat/{username}")
async def chat_endpoint(websocket: WebSocket, username: str, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            new_text = models.Message(username=username, content=data)
            db.add(new_text)
            db.commit()
            db.refresh(new_text)
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get("/messages")
def get_all_messages_by_users(db: Session = Depends(get_db)):
   all_Data= db.query(models.Message).all()
   return all_Data
