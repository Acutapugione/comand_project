import requests
from config import bot_token, code_to_smile_eu
from start import dp
from weatherstate import WeatherState
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram import types
from databas.models_ import PrognosToday
from start import session
from choise_button import todey_id


@dp.callback_query(F.data == "prognos_todey")
async def get_weather(query: types.Message, state: FSMContext):
    try:
        state_data = await state.get_data()
        user_city = state_data.get('city')
        today_data = session.query(PrognosToday).filter_by(city=user_city).all()
        for row in today_data:
            weather_descriptions = row.weather_description.split(', ')
            wd = [code_to_smile_eu[desc] if desc in code_to_smile_eu else "Подивися в вікно, а то і сам я не зрозумію" for desc in weather_descriptions]

            reply_text = (
                f'Часова мітка: {row.timestamp}\n'
                f'Місто: {row.city}\n'
                f'Країна: {row.country}\n'
                f'Опис погоди: {", ".join(weather_descriptions)}   {", ".join(wd)}\n'
                f'Температура: {row.temperature} C°\n'
                f'Швидкість вітру: {row.wind_speed}\n'
                f'Напрямок вітру: {row.wind_direction}\n'
                f'Тиск: {row.pressure}'
            )
            await query.message.answer(reply_text,  reply_markup=todey_id)
            await state.clear()
            #await query.message.delete()

    except Exception as e:
        print(f"An error occurred: {e}")
        await query.message.reply('Провірте назву міста або сталася помилка')

async def main():
    bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher()
    dispatcher.include_router(dp)

    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    