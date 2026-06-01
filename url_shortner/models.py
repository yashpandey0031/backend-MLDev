from sqlalchemy import Column, Integer, String
from database import Base


class longUrls(Base):
  __tablename__ = "longurls"
  id = Column(Integer, primary_key = True, index = True)
  url=Column(String, nullable = False)
  generated_code = Column(String, nullable = False)