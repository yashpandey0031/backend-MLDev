from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import secrets
from fastapi.responses import RedirectResponse

router = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post("/shorten")
def shorten_longURL(url: str,db: Session = Depends(get_db)):
  code = secrets.token_urlsafe(5)
  new_entry = models.longUrls(url = url, generated_code = code)
  db.add(new_entry)
  db.commit()
  db.refresh(new_entry)
  return code #get the code after shortening theurl in order to use it in the later part 

@router.get("/{code}")
def redirect_code(code: str,db: Session = Depends(get_db)):
  full_url = db.query(models.longUrls).filter(models.longUrls.generated_code == code).first()

  if full_url is None:
      raise HTTPException (status_code=404, detail="No such url with this code exists")
  
  return RedirectResponse(url=full_url.url)

#we are using this for redirecting dats crazy chat yk the redirectresponse one 