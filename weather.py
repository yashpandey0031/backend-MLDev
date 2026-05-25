from fastapi import FastAPI
import httpx
app = FastAPI()

@app.get("/weather/{city}")
def read_weather(city: str ):
  your_key  = "044c34c640d3efd97ec786376f753416"
  weather = httpx.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={your_key}&units=metric")

  


  return{f"weather in {city}": weather.json()}