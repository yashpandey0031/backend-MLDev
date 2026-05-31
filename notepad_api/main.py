from fastapi import FastAPI
from database import engine
from routers import notes, auth


import models


models.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(notes.router)
app.include_router(auth.router)