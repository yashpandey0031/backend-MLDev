# id
# title
# content
# created_At
# updated_at
#orm is a programming technique to interact with the database insetead of writing sql everytime
from sqlalchemy import Column, Integer, String, DataTime 
from database import Base
import datetime

class Note(Base):
  __tablename__ = "notes"
  id = Column(Integer, primary_key = True,index= True)
  title = Column(String, nullable = False)
  content = Column(String, nullable = False)
  created_at = Column(DataTime, default = datetime.datetime.utcnow)
  updated_at = Column(DataTime, default = datetime.datetime.utcnow, onupdate=datetime.utcnow)
  


