from choise_button import choice, start
from config import bot_token
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types
from weatherstate import WeatherState
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databas.models_ import PrognosToday, PrognosTodayId, Base, PrognosForecastDays
from datetime import datetime
import requests


dp = Router()

engine = create_engine('sqlite:///./weather.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@dp.message(CommandStart())
async def start_1(message: types.Message, state: FSMContext):
    await message.answer(text='Привіт. Я бот, який покаже тобі погоду на день і місто, яке ти вибереш. Введи місто:', reply_markup=start)
    await state.set_state(WeatherState.city)

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_1(message: types.Message, state: FSMContext):
    await state.clear()
    await message.message.answer(text='Напиши нове місто:', reply_markup=start)
    await state.set_state(WeatherState.city)
    

@dp.message(WeatherState.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.clear()
    await state.update_data(city=message.text)
    await message.reply('Виберіть на який день чи тиждень ви хочете подивитися погоду:', reply_markup=choice)
    state_data = await state.get_data()
    user_city = state_data.get('city')
    await some_function_that_needs_user_city(user_city)

async def some_function_that_needs_user_city(user_city: str):
    session.query(PrognosToday).delete()
    session.query(PrognosTodayId).delete()
    session.query(PrognosForecastDays).delete()
    session.commit()
    r = requests.get(f'http://api.weatherstack.com/current?access_key=588131fccadc25dc232cff82b281bc5c&query={user_city}')
    data = r.json()

    today_info = {
        'city': user_city,
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
    
    r = requests.get(f'http://api.weatherstack.com/forecast?access_key=588131fccadc25dc232cff82b281bc5c&query=fetch:ip')
    data = r.json()
    
    today_id_info = {
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

    for day_data in data['data']:
        day_info = {
            'city': data['city_name'],
            'temperature_min': day_data['min_temp'],
            'temperature_max': day_data['max_temp'],
            'wind_speed': day_data['wind_spd'],
            'wind_direction': day_data['wind_cdir_full'],
            'pressure': day_data['pres'],
            'timestamp': datetime.utcnow(),
        }

        prognos_forecast_day = PrognosForecastDays(**day_info)
        session.add(prognos_forecast_day)

    session.commit()



async def main():
    bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher()
    dispatcher.include_router(dp)

    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

