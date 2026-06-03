from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime


class Message(Base):
  __tablename__ = "Message"
  id = Column(Integer, primary_key = True, index = True)
  username = Column(String, nullable = False)
  content=Column(String, nullable = False)
  created_at = Column(DateTime, default = datetime.now)