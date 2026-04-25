from fastapi import FastAPI
app = FastAPI()


@app.get("/")
def read_root():
  return("Hello this is my first API with FastAPI/This is so stupid")