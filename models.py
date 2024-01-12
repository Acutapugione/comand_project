from pydantic import BaseModel
from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, Float, DateTime, String
from database_t import Base
from sqlalchemy.orm import Mapped, mapped_column

class PrognosForecastDays(Base):
    __tablename__ = 'prognos_forecast_days'

    id = Column(Integer, primary_key=True)
    city = Column(String) 
    date = Column(DateTime, default=datetime.utcnow)
    temperature_min = Column(Float)
    temperature_max = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    pressure = Column(Float)

class PrognosToday(Base):
    __tablename__ = 'prognos_today'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    country = Column(String)
    weather_description = Column(String)
    temperature = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    pressure = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class PrognosTodayId(Base):
    __tablename__ = 'prognos_today_id'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    country = Column(String)
    datetime = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    pressure = Column(Float)
