from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from passlib.context import CryptContext
import models

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
#opens a database sesion , gives it a endpoint and closes it when done , every endpoint has to use this 
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post("/register")
def register_account(username: str, password: str, db: Session = Depends(get_db)):

  newuser = db.query(models.User).filter(models.User.username == username).first()
    
  if newuser:
        raise HTTPException(status_code=400, detail="username already taken")

  newuser = models.User(username = username, hashed_password=pwd_context.hash(password)) #here password is the one that user types and we store its hashed version into hashed_password
  db.add(newuser)
  db.commit()
  db.refresh(newuser)
  return {"message": "Account created successfully"}



