from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from routers.auth import get_current_user
from datetime import datetime
import os

router = APIRouter()


#opens a database sesion , gives it a endpoint and closes it when done , every endpoint has to use this 
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def activity_log(titleo: str, created_ato: datetime):
    with open("activity.log", "a", encoding="utf-8") as file:
        file.write(f"Note created at: {created_ato} Note created title: {titleo}\n")
    os.remove("notes.db")

   

@router.post("/notes")
def create_note(title: str, content: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user),):
  new_note = models.Note(title = title, content=content, user_id=current_user.id)
  db.add(new_note) 
  db.commit()
  db.refresh(new_note) #refresh to get date and id
  background_tasks.add_task(activity_log,new_note.title,new_note.created_at)
  return new_note

@router.get("/notes")
def get_all_notes(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
  all_notes = db.query(models.Note).filter(models.Note.user_id == current_user.id).all()
  return all_notes

@router.get("/notes/{id}") #use {} to make it dynamic and not a literal
def get_note_by_id(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
  note = db.query(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id).first()
  #first() only give the first item and unwrap it
  return note

@router.delete("/notes/{id}")
def delete_note_by_id(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id).first()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}


@router.put("/notes/{id}")
def update_note_by_id(id: int,title: str,content: str, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
   note=db.query(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id).first()

   if note is None:
      raise HTTPException(status_code=404,detail="Note not found")
   history_note_copy = models.History(note_id=note.id, title = note.title,content=note.content) #saving the old note by id 
   db.add(history_note_copy)

   note.title = title
   note.content = content
   db.commit()
   db.refresh(note)
   return note
   
@router.get("/notes/{id}/history")
def fetch_note_history_by_id(id: int,db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
   history = db.query(models.History).filter(models.History.note_id == id).all()

   if not history :
    raise HTTPException(status_code=404,detail="No history found for this")

   return history

#here we are fetching the history database for any entries with similar note_id and then just printing them
#as for if not history , its coz since all there will always be a list even if empty 
