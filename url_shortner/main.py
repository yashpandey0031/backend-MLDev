from fastapi import FastAPI
from database import engine
from routers import short_urls


import models


models.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(short_urls.router)
