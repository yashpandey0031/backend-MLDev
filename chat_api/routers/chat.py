from fastapi import APIRouter, WebSocket , Depends, HTTPException, UploadFile,File
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import asyncio
import shutil
import os

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


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    #file type check coz why not fuck yeah
    allowed_types=["application/pdf"]
    if file.content_type not in allowed_types:
       raise HTTPException(status_code=400, detail="only pdfs are allowed")
    
    #  extension = os.path.splitext(file.filename)[1]  # gets .jpg, .png etc
    # unique_filename = f"{uuid.uuid4()}{extension}"  # e.g. a1b2c3d4.jpg
    
    folder_name = "uploads"
    file_path=f"{folder_name}/{file.filename}"
    with open(file_path,"wb") as buffer:
       shutil.copyfileobj(file.file,buffer)
    return {"filename": file.filename, "url" : f"/uploads/{file.filename}"}
