from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databas.models_ import PrognosToday, PrognosTodayId, Base, PrognosForecastDays
from datetime import datetime
import requests
from start import WeatherState


user_city = WeatherState.city

print(user_city)
engine = create_engine('sqlite:///./weather.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.query(PrognosToday).delete()
session.query(PrognosTodayId).delete()
session.query(PrognosForecastDays).delete()
session.commit()

r = requests.get(f'http://api.weatherstack.com/current?access_key=588131fccadc25dc232cff82b281bc5c&query={user_city}')
data = r.json()

today_info = {
    'city': data["location"]["name"],
    'country': data["location"]["country"],
    'weather_description': ', '.join(data["current"]["weather_descriptions"]),
    'temperature': data["current"]["temperature"],
    'wind_speed': data["current"]["wind_speed"],
    'wind_direction': data["current"]["wind_dir"],
    'pressure': data["current"]["pressure"],
    'timestamp': datetime.utcnow(),
}

prognos_today = PrognosToday(**today_info)

session.add(prognos_today)
session.commit()

r = requests.get(f'http://api.weatherstack.com/current?access_key=588131fccadc25dc232cff82b281bc5c&query={user_city}')
data = r.json()

today_id_info = {
    'city': data["location"]["name"],
    'country': data["location"]["country"],
    'datetime': datetime.utcnow(),
    'temperature': data["current"]["temperature"],
    'wind_speed': data["current"]["wind_speed"],
    'wind_direction': data["current"]["wind_dir"],
    'pressure': data["current"]["pressure"],
}

prognos_today_id = PrognosTodayId(**today_id_info)

session.add(prognos_today_id)
session.commit()

r = requests.get(f'https://api.weatherbit.io/v2.0/forecast/daily?city={user_city}&key=e39f46499b9847acb52ed01846838cce&days=7&lang=uk')
data = r.json()

for day_data in data.get("data", []):

    day_info = {
        'city': data["city_name"],
        'date': datetime.utcfromtimestamp(day_data["ts"]),
        'temperature_min': day_data["min_temp"],
        'temperature_max': day_data["max_temp"],
        'wind_speed': day_data["wind_spd"],
        'wind_direction': day_data["wind_cdir_full"],
        'pressure': day_data["pres"],
    }

    prognos_forecast_day = PrognosForecastDays(**day_info)
    session.add(prognos_forecast_day)
    session.commit()