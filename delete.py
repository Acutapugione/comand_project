from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine('sqlite:///./weather.db')
Base.metadata.create_all(bind=engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


class PrognosForecastDays(Base):
    __tablename__ = 'prognos_forecast_days'

    id = Column(Integer, primary_key=True)
    city = Column(String)  # Assuming 'city' should be a string
    #weather_description = Column(String)
    temperature_min = Column(Float)  # Add temperature_min column
    temperature_max = Column(Float)  # Add temperature_max column
    wind_speed = Column(Float)
    wind_direction = Column(String)
    pressure = Column(Float)
    timestamp = Column(DateTime)

# Видаліть існуючу таблицю, якщо вона існує
Base.metadata.drop_all(bind=engine, tables=[PrognosForecastDays.__table__])

# Створіть таблицю знову
Base.metadata.create_all(bind=engine, tables=[PrognosForecastDays.__table__])

