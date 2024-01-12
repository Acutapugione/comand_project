from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databas.models_ import PrognosForecastDays, Base
from datetime import datetime
import requests

engine = create_engine('sqlite:///./weather.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

user_city = "Kyiv"
r = requests.get(f'https://api.weatherbit.io/v2.0/forecast/daily?city={user_city}&key=e39f46499b9847acb52ed01846838cce&days=16&lang=uk')
data = r.json()

for day_data in data["data"]:
    day_info = {
        'city': data["city_name"],
        'date': datetime.utcfromtimestamp(day_data["ts"]),
        'temperature_min': day_data["min_temp"],
        'temperature_max': day_data["max_temp"],
        'wind_speed': day_data["wind_spd"],
        'wind_direction': day_data["wind_cdir_full"],
        'pressure': day_data["pres"],
    }
    prognos_day = PrognosForecastDays(**day_info)
    session.add(prognos_day)

session.commit()
