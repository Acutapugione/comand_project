from sqlalchemy import Column, Integer, Float, DateTime
from database import Base
from datetime import datetime

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    temperature_2m = Column(Float)
    relative_humidity_2m = Column(Float)
    pressure_msl = Column(Float)
