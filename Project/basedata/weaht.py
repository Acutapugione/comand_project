import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Mapped,mapped_column
from weather_data import w1,w2

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id: Mapped[Integer] = mapped_column(primary_key=True)
    date: Column[DateTime]
    temperature_2m: Column[Float]
    relative_humidity_2m:Column[Float]
    surface_pressure: Column[Float]


engine = create_engine('sqlite:///weather_data.db')


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": w1,
    "longitude": w2,
    "start_date": "w1",
    "end_date": "w2",
    "hourly": ["temperature_2m", "relative_humidity_2m", "surface_pressure"],
    "interval": "1h"
}


responses = openmeteo.weather_api(url, params=params)


for response in responses:
    coordinates = f"Coordinates {response.Latitude()}°E {response.Longitude()}°N"
    elevation = f"Elevation {response.Elevation()} m asl"
    timezone = f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}"
    utc_offset = f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s"
    
    print(coordinates)
    print(elevation)
    print(timezone)
    print(utc_offset)

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(2).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly_temperature_2m,
        "relative_humidity_2m": hourly_relative_humidity_2m,
        "surface_pressure": hourly_surface_pressure
    }


    hourly_dataframe = pd.DataFrame(data=hourly_data)


    hourly_dataframe.to_sql('weather_data', con=engine, if_exists='append', index=False)



session.close()
