from fastapi import FastAPI
from database import engine
from routers import background


import models


models.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(background.router)
