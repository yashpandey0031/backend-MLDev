from sqlalchmey import create_engine
from sqlalchmey.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///.notepad_api/notes.db"

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind = engine)
Base = declarative_base()