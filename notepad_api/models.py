# id
# title
# content
# created_At
# updated_at
#orm is a programming technique to interact with the database insetead of writing sql everytime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from database import Base
from datetime import datetime

class Note(Base):
  __tablename__ = "notes"
  id = Column(Integer, primary_key = True,index= True)
  title = Column(String, nullable = False)
  content = Column(String, nullable = False)
  created_at = Column(DateTime, default = datetime.now)
  updated_at = Column(DateTime, default = datetime.now, onupdate=datetime.now)


  #foreign key is a link between history and notes, title , content , saved_at are there own independent columns
  
class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id"))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    saved_at = Column(DateTime, default=datetime.now)

class User(Base):
   __tablename__ = "user"

   id = Column(Integer, primary_key =  True, index = True)
   username = Column(String,nullable = False, unique = True)
   hashed_password = Column(String,nullable = False) 
   is_active = Column(Boolean, default =  True) #for setting the account as active or not 

  


