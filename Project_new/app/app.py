import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from sqlalchemy.orm import sessionmaker
from models import WeatherData
from database import engine
from datetime import datetime
from database import SessionLocal

cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

async def get_and_store_weather_data(request):
    # ... (остальной код без изменений)

    db = SessionLocal()
    try:
        for _, row in hourly_dataframe.iterrows():
            weather_data = WeatherData(
                date=row['date'],
                temperature_2m=row['temperature_2m'],
                relative_humidity_2m=row['relative_humidity_2m'],
                pressure_msl=row['pressure_msl']
            )
            db.add(weather_data)
        db.commit()
    finally:
        db.close()
