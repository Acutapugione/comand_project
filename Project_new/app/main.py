from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from app import get_and_store_weather_data
from models import WeatherDataResponse, WeatherDataRequest

app = FastAPI()

@app.post("/weather_data/", response_model=List[WeatherDataResponse])
async def weather_data(request: WeatherDataRequest):
    return await get_and_store_weather_data(request)
