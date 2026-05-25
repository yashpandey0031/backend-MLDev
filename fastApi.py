from fastapi import FastAPI
import random as r

app = FastAPI()
@app.get("/randomjoke")
def read_randomjoke():
    jokes=[
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "What do you call a bear with no teeth? A gummy bear!"
    ]

    joke = r.choice(jokes)
    return {"joke of the day isss":joke}