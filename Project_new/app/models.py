from pydantic import BaseModel
from datetime import datetime
from typing import List

class WeatherDataRequest(BaseModel):
    latitude: float
    longitude: float
    start_date: str
    end_date: str

class WeatherDataResponse(BaseModel):
    date: datetime
    temperature_2m: float
    relative_humidity_2m: float
    pressure_msl: float
