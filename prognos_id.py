import requests
from config import bot_token
from prognos_todae import dp
from weatherstate import WeatherState
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram import types
from databas.models_ import PrognosTodayId
from start import session
from choise_button import todey_id
from aiogram.fsm.context import FSMContext


@dp.callback_query(F.data == "prognos_id")
async def get_weather(query: types.Message, state: FSMContext):
    try:
        today_data_id = session.query(PrognosTodayId).all()
        for row in today_data_id:
            reply_text = (
                f'Часова мітка: {row.datetime}\n'
                f'Країна: {row.country}\n'
                f'Температура: {row.temperature} C°\n'
                f'Швидкість вітру: {row.wind_speed}\n'
                f'Напрямок вітру: {row.wind_direction}\n'
                f'Тиск: {row.pressure}'
            )
            await query.message.answer(reply_text, reply_markup=todey_id)
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
