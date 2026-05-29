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
  new_note = models.Note(title = title, content=content)
  db.add(new_note)
  db.commit()
  db.refresh(new_note) #refresh to get date and id
  return new_note

@router.get("/notes")
def get_all_notes(db: Session = Depends(get_db)):
  all_notes = db.query(models.Note).all()
  return all_notes

@router.get("/notes/{id}") #use {} to make it dynamic and not a literal
def get_note_by_id(id: int, db: Session = Depends(get_db)):
  note = db.query(models.Note).filter(models.Note.id == id).first()
  return note