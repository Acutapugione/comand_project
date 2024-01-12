from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_ import PrognosForecastDays, PrognosToday, PrognosTodayId, Base

# Assuming you have created the engine and bound it to the Base
engine = create_engine('sqlite:///./weather.db')
Base.metadata.create_all(bind=engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Query and print data for PrognosForecastDays table
forecast_days_data = session.query(PrognosForecastDays).all()
print("PrognosForecastDays Table:")
for row in forecast_days_data:
    print(f"id: {row.id}, city: {row.city}, timestamp: {row.timestamp}, temperature_min: {row.temperature_min}, temperature_max: {row.temperature_max}, wind_speed: {row.wind_speed}, wind_direction: {row.wind_direction}, pressure: {row.pressure}")

# Query and print data for PrognosToday table
today_data = session.query(PrognosToday).all()
print("\nPrognosToday Table:")
for row in today_data:
    print(f"id: {row.id}, city: {row.city}, country: {row.country}, weather_description: {row.weather_description}, temperature: {row.temperature}, wind_speed: {row.wind_speed}, wind_direction: {row.wind_direction}, pressure: {row.pressure}, timestamp: {row.timestamp}")

# Query and print data for PrognosTodayId table
today_id_data = session.query(PrognosTodayId).all()
print("\nPrognosTodayId Table:")
for row in today_id_data:
    print(f"id: {row.id}, country: {row.country}, datetime: {row.datetime}, temperature: {row.temperature}, wind_speed: {row.wind_speed}, wind_direction: {row.wind_direction}, pressure: {row.pressure}")

# Close the session
session.close()
