from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/id/{item_id}")
def read_item_by_id(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/items/name/{item_name}")
def read_item_by_name(item_name: str | None = None):
    return {item_name + " were sold yesterday"}

@app.get("/aboutme")
def read_aboutme():
    return {"hello my name is yash pandey and this is my attempt at learning about fast api"}