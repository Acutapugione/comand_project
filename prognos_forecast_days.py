import requests
import io
import asyncio
from prognos_id import dp
from weatherstate import WeatherState
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
import matplotlib.pyplot as plt
from config import bot_token, code_to_smile_eu
from choise_button import f_d_p, f_d_t, f_d_w_s, f_d_w_d, f_d_pr
from databas.models_ import PrognosForecastDays
from start import session


# @dp.callback_query((F.data == "prognos_forecast_days") | (F.data == "back_2"))
# async def forecast_days_pogoda(query: types.CallbackQuery, state: FSMContext):
#     try:
#         state_data = await state.get_data()
#         user_city = state_data.get('city')
#         today_data_forecast_days = session.query(PrognosForecastDays).filter_by(city=user_city).all()
#         for row in today_data_forecast_days:
#             weather_descriptions = row.weather_description.split(', ')
#             wd = [code_to_smile_eu[desc] if desc in code_to_smile_eu else "Подивися в вікно, а то і сам я не зрозумію" for desc in weather_descriptions]
#             reply_text = (
#                 f'Часова мітка: {row.datetime}\n'
#                 f'Місто: {row.city}\n'
#                 f'Опис погоди: {", ".join(weather_descriptions)}   {", ".join(wd)}\n'
#             )
#         await query.message.answer(reply_text, reply_markup=f_d_p)
#         await query.message.delete()

#     except Exception as e:
#         print(e)
#         await query.message.reply('Перевірте назву міста')

@dp.callback_query((F.data == "prognos_forecast_days") | (F.data == "back_3"))
async def forecast_days_temperature(query: types.CallbackQuery, state: FSMContext):
    try:
        state_data = await state.get_data()
        user_city = state_data.get('city')
        today_data = session.query(PrognosForecastDays).filter_by(city=user_city).all()
        
        temperatures_max = []
        temperatures_min = []

        for row in today_data:
            temperature_max = row.temperature_max
            temperature_min = row.temperature_min
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
    try:
        state_data = await state.get_data()
        user_city = state_data.get('city')
        today_data = session.query(PrognosForecastDays).filter_by(city=user_city).all()
        
        wind_speeds = []

        for row in today_data:
            wind_speed = row.wind_speed
            wind_speeds.append(wind_speed)
        plt.plot(wind_speeds, color='red', linewidth=2, linestyle='solid', label='Швидкість вітру',  marker = 'o',markevery = 1)
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

    except Exception as e:
        print(e)
        await query.message.reply('Перевірте назву міста')

@dp.callback_query((F.data == "further_3") | (F.data == "back_5"))
async def forecast_days_wind_dir(query: types.CallbackQuery, state: FSMContext):
    try:
        state_data = await state.get_data()
        user_city = state_data.get('city')
        today_data_forecast_days = session.query(PrognosForecastDays).filter_by(city=user_city).all()
         
        reply_text = ""
        for row in today_data_forecast_days:
            reply_text += (
                f'Часова мітка: {row.timestamp}\n'
                f'Місто: {row.city}\n'
                f'Опис погоди: {row.wind_direction}\n'
            )
         
        await query.message.answer(reply_text, reply_markup=f_d_w_d)
        await query.message.delete()

    except Exception as e:
        print(f"An error occurred: {e}")
        await query.message.reply('Перевірте назву міста або сталася помилка')


@dp.callback_query((F.data == "further_4"))
async def forecast_days_pres(query: types.CallbackQuery, state: FSMContext):
    try:
        state_data = await state.get_data()
        user_city = state_data.get('city')
        today_data = session.query(PrognosForecastDays).filter_by(city=user_city).all()
        
        pressures = []

        for row in today_data:
            pressure = row.pressure
            pressures.append(pressure)
        plt.plot(pressures, color='red', linewidth=2, linestyle='solid', label='Тиск',  marker = 'o',markevery = 1)
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
