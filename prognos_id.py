import requests
from config import bot_token, code_to_smile_eu
import asyncio
from prognos_todae import dp
from weatherstate import WeatherState
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram import types


@dp.callback_query(F.data=="prognos_id")
async def get_weathe(message: types.Message):
    try:
        r = requests.get(f'http://api.weatherstack.com/forecast?access_key=588131fccadc25dc232cff82b281bc5c&query=fetch:ip')
        data = r.json()
        localtime = data["location"]["localtime"]
        country = data["location"]["country"]
        weather_descriptions = data["current"]["weather_descriptions"]
        wd = [code_to_smile_eu[desc]
              if desc in code_to_smile_eu
              else "Подивися в вікно, а то і сам я не зрозумію" for desc in weather_descriptions
              ]
        temperature = data["current"]["temperature"]
        wind_speed = data["current"]["wind_speed"]
        wind_dir = data["current"]["wind_dir"]
        pressure = data["current"]["pressure"]

        await message.message.reply(f'***{localtime}***\nКраїна: {country}\n'
                            f'Яка буде сьогодні погода: {weather_descriptions} {wd}\n'
                            f'Температура: {temperature} C°\nШвидкість вітру: {wind_speed}\n'
                            f'В яку сторону дує вітер: {wind_dir}\nТиск: {pressure}')

    except:
        await message.message.reply('Провірте назву міста')

async def main():
    bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher()
    dispatcher.include_router(dp)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
