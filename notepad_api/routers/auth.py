from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from passlib.context import CryptContext
from jose import jwt
import models
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()
SECRET_KEY = "j8kL2mN9pQ4rS7tU1vW6xY3zA5bC0dE"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


#opens a database sesion , gives it a endpoint and closes it when done , every endpoint has to use this 
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        user = db.query(models.User).filter(models.User.id == user_id).first()
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

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



from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

@router.post("/login")
def login_into_account(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    finduser = db.query(models.User).filter(models.User.username == form_data.username).first()

    if finduser is None:
        raise HTTPException(status_code=404, detail="No user found with that username")
    
    if not pwd_context.verify(form_data.password, finduser.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    payload = {"user_id": finduser.id}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
   
#token that we get is basically a payload with all the info that we need to provide , in this case we need to vreify the user so we check the user id and its 1 in this case

