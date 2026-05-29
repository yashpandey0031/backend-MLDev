from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models

router = APIRouter()


#opens a database sesion , gives it a endpoint and closes it when done , every endpoint has to use this 
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post("/notes")
def create_note(title: str, content: str, db: Session = Depends(get_db)):
  

