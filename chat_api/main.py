from fastapi import FastAPI
from database import engine
from routers import chat
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import models
models.Base.metadata.create_all(bind = engine)
app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"),name = "uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat.router)
