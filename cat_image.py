from fastapi import FastAPI
import httpx
app = FastAPI()

@app.get("/cat")
def get_cat_image():
  cat_image = httpx.get(f"https://api.thecatapi.com/v1/images/search")
  data = cat_image.json()
  # only_image = {"Cat_image" : data[0]["url"]}
  # return {"URL" : only_image}
  return {"cat_image":data[1]["url"]} #we are using data[0] as the first element of the list 

