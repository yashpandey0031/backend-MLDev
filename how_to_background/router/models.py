from sqlalchemy import Column, Integer, String
from database import Base


class user(Base):
  __tablename__ = "longurls"
  id = Column(Integer, primary_key = True, index = True)
  url=Column(String, nullable = False)
  generated_code = Column(String, nullable = False)