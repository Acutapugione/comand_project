import requests
import io
import asyncio
from prognos_id import dp
from weatherstate import WeatherState
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
import matplotlib.pyplot as plt
from config import bot_token, code_to_smile_uk
from choise_button import f_d_p, f_d_t, f_d_w_s, f_d_w_d, f_d_pr


@dp.callback_query((F.data == "prognos_forecast_days") | (F.data == "back_2"))
async def forecast_days_pogoda(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    user_city = state_data.get('city')
    try:
        r = requests.get(f'https://api.weatherbit.io/v2.0/forecast/daily?city={user_city}&key=e39f46499b9847acb52ed01846838cce&days=16&lang=uk')
        data = r.json()
        weather_statuses = []

        for i in range(1, 8):
            weather_data = data["data"][i]
            date = weather_data["datetime"]
            weather_description = weather_data["weather"]["description"]
            wd = code_to_smile_uk.get(weather_description, "подивися в вікно, а то і сам я не зрозумію")
    
            weather_statuses.append(f'Погода в місті {user_city} на {date}:\nПогода: {weather_description},   {wd}' )
        await query.message.answer('\n\n'.join(weather_statuses), reply_markup=f_d_p)
        await query.message.delete()

    except Exception as e:
        print(e)
        await query.message.reply('Перевірте назву міста')

@dp.callback_query((F.data == "further_1") | (F.data == "back_3"))
async def forecast_days_temperature(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    user_city = state_data.get('city')
    try:
        r = requests.get(f'https://api.weatherbit.io/v2.0/forecast/daily?city={user_city}&key=e39f46499b9847acb52ed01846838cce&days=16')
        data = r.json()
        temperatures_max = []
        temperatures_min = []

        for i in range(1, 8):
            weather_data = data["data"][i]
            temperature_min = weather_data["min_temp"]
            temperature_max = weather_data["max_temp"]
            temperatures_max.append(temperature_max)
            temperatures_min.append(temperature_min)
        plt.plot(temperatures_max, color='red', linewidth=2, linestyle='solid', label='Максимальна температура',  marker = 'o',markevery = 1)
        plt.plot(temperatures_min, color='blue', linewidth=2, linestyle='solid', label='Мінімальна температура',  marker = 'o',markevery = 1)
        plt.title('Температура на 7 днів вперед')
        plt.xlabel('День')
        plt.ylabel('Температура')
        plt.grid(True)
        plt.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        buf.name = 'temperature_plot.png'
        buf.seek(0)
        await query.message.answer_photo(photo=types.BufferedInputFile(buf.getvalue(), filename='temperature_plot.png'), caption='Графік температури', reply_markup=f_d_t)
        await query.message.delete()
        buf.close()
        buf = io.BytesIO()
        # for weather_message in weather_messages:
        #     await query.message.edit_text(weather_message)

    except Exception as e:
        print(e)
        await query.message.reply('Перевірте назву міста')

@dp.callback_query((F.data == "further_2") | (F.data == "back_4"))
async def forecast_days_wind_speed(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    user_city = state_data.get('city')
    try:
        r = requests.get(f'https://api.weatherbit.io/v2.0/forecast/daily?city={user_city}&key=e39f46499b9847acb52ed01846838cce&days=16')
        data = r.json()
        wind_speed_list = []
        weather_messages = []

        for i in range(1, 8):
            weather_data = data["data"][i]
            speed = weather_data["wind_spd"]
            wind_speed_list.append(speed)

        plt.plot(wind_speed_list, color='blue', linewidth=2, linestyle='solid', label='Швидкість вітру',  marker = 'o',markevery = 1)
        plt.title('Швидкість вітру на 7 днів вперед')
        plt.xlabel('День')
        plt.ylabel('Швидкість вітру')
        plt.grid(True)
        plt.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        buf.name = 'wind_speed.png'
        buf.seek(0)
        await query.message.answer_photo(photo=types.BufferedInputFile(buf.getvalue(), filename='wind_speed.png'), caption='Графік швидкості вітру', reply_markup=f_d_w_s)
        await query.message.delete()
        buf.close()
        buf = io.BytesIO()
        # for weather_message in weather_messages:
        #     await query.message.reply(weather_message)

    except Exception as e:
        print(e)
        await query.message.reply('Перевірте назву міста')

@dp.callback_query((F.data == "further_3") | (F.data == "back_5"))
async def forecast_days_wind_dir(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    user_city = state_data.get('city')
    try:
        r = requests.get(f'https://api.weatherbit.io/v2.0/forecast/daily?city={user_city}&key=e39f46499b9847acb52ed01846838cce&days=16&lang=uk')
        data = r.json()
        weather_statuses = []

        for i in range(1, 8):
            weather_data = data["data"][i]
            date = weather_data["datetime"]
            wind_cdir_full = weather_data["wind_cdir_full"]
    
            weather_statuses.append(f'Напрямок вітру в місті {user_city} на {date}:\nНапрамок вітру: {wind_cdir_full}' )
            
        await query.message.answer('\n\n'.join(weather_statuses), reply_markup=f_d_w_d)
        await query.message.delete()

    except Exception as e:
        print(e)
        await query.message.reply('Перевірте назву міста')

@dp.callback_query((F.data == "further_4"))
async def forecast_days_pres(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    user_city = state_data.get('city')
    try:
        r = requests.get(f'https://api.weatherbit.io/v2.0/forecast/daily?city={user_city}&key=e39f46499b9847acb52ed01846838cce&days=16')
        data = r.json()
        pressure = []
        weather_messages = []

        for i in range(1, 8):
            weather_data = data["data"][i]
            pres = weather_data["pres"]
            pressure.append(pres)

        plt.plot(pressure, color='blue', linewidth=2, linestyle='solid', label='Тиск', marker = 'o',markevery = 1)
        plt.title('Тиск на 7 днів вперед')
        plt.xlabel('День')
        plt.ylabel('Тиск')
        plt.grid(True)
        plt.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        buf.name = 'pres.png'
        buf.seek(0)
        await query.message.answer_photo(photo=types.BufferedInputFile(buf.getvalue(), filename='pres.png'), caption='Графік тиску', reply_markup=f_d_pr)
        await query.message.delete()
        buf.close()
        buf = io.BytesIO()
        for weather_message in weather_messages:
            await query.message.reply(weather_message)

    except Exception as e:
        print(e)
        await query.message.reply('Перевірте назву міста')

async def main():
    bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher()
    dispatcher.include_router(dp)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
