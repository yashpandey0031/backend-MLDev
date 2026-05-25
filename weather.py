from fastapi import FastAPI
import httpx
app = FastAPI()

@app.get("/weather/{city}")
def read_weather(city: str ):
  your_key  = "044c34c640d3efd97ec786376f753416"
  weather = httpx.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={your_key}&units=metric")

  data = weather.json()
  cleaned_data = {
    "temperature": data["main"]["temp"],
    "description": data["weather"][0]["description"],
    "wind_speed": data["wind"]["speed"]
  }

  return{f"weather in {city}": cleaned_data}

# output ->
# {
#   "weather in russia": {
#     "temperature": 5.96,
#     "description": "overcast clouds",
#     "wind_speed": 4.56
#   }
# }