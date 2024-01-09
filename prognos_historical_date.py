import requests
from choise_button import choice
from config import bot_token
import asyncio
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime


dp = Router()

class WeatherState(StatesGroup):
    city = State()
    start_date = State()
    end_date = State()

@dp.message(CommandStart())
async def send_predictions(message: types.Message, state: FSMContext):
    await message.answer(text='Привіт. Я бот, який покаже тобі погоду на день і місто, яке ти вибереш. Введи місто:')
    await state.set_state(WeatherState.city)

@dp.message(WeatherState.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.clear()
    await state.update_data(city=message.text)
    await message.reply('Виберіть на який день чи тиждень ви хочете подивитися погоду:', reply_markup=choice)


@dp.callback_query(F.data == "prognos_historical_date")
async def process_historical_date(callback_query: types.CallbackQuery, state: FSMContext):
    message_text = callback_query.message.text
    button_text = callback_query.data
    await state.update_data(city=message_text)
    await callback_query.message.reply('Введи початкову дату у форматі YYYY-MM-DD:')
    await state.set_state(WeatherState.start_date)


@dp.message(WeatherState.start_date)
async def process_end_date(message: types.Message, state: FSMContext):
    try:
        start_date = datetime.strptime(message.text, '%Y-%m-%d')
        await state.update_data(start_date=start_date)
        await message.reply('Введи кінцеву дату у форматі YYYY-MM-DD:')
        await state.set_state(WeatherState.end_date)
    except ValueError:
        await message.reply('Некоректний формат дати. Спробуйте ще раз.')

@dp.message(WeatherState.end_date)
async def result(message: types.Message, state: FSMContext):
    try:
        end_date = datetime.strptime(message.text, '%Y-%m-%d')
        await state.update_data(end_date=end_date)
        
        state_data = await state.get_data()
        user_city = state_data.get('city')
        start_date = state_data.get('start_date')
        end_date = state_data.get('end_date')
        
        r = requests.get(f'https://api.weatherbit.io/v2.0/history/daily?city={user_city}&start_date={start_date}&end_date={end_date}&key=e39f46499b9847acb52ed01846838cce')
        data = r.json()

        if "data" in data and data["data"]:
            for day_data in data["data"]:
                max_temp = day_data["max_temp"]
                min_temp = day_data["min_temp"]
                wind_speed = day_data["wind_spd"]
                wind_dir = day_data["wind_dir"]
                pressure = day_data["pres"]

                await message.reply(f'***{day_data["datetime"]}***\nПогода в місті: {user_city}\n'
                                    f'Максимальна температура: {max_temp} C°\nМінімальна температура: {min_temp} C°\n'
                                    f'Швидкість вітру: {wind_speed}\nВ яку сторону дує вітер: {wind_dir}\nТиск: {pressure}')

        else:
            await message.reply('Виникла помилка при отриманні погоди')

    except ValueError:
        await message.reply('Некоректний формат даних від API. Спробуйте ще раз.')
    except Exception as e:
        print(e)
        await message.reply(f'Виникла помилка при отриманні погоди: {str(e)}')


async def main():
    bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher()
    dispatcher.include_router(dp)

    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
