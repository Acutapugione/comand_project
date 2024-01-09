import json
import logging
from choise_button import choice
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import matplotlib.pyplot as plt
import io
import requests
from config import open_weather_token, bot_token
from sqlalchemy_r.sqlalchemy_test import city


bot = Bot(token=bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_predictions(message: types.Message):
    await message.answer(text='Привіт. Я бот який покаже тобі погоду на день і місто яке ти вибереш. Напиши місто:', reply_markup=choice)

@dp.message_handler(commands=['suport'])
async def send_predictions(message: types.Message):
    await message.answer(text='Telegram: https://t.me/Phonk_Top_Amor\nDiscord: amor_top_1')

def get_predictions():
    x1 = [1, 2, 3, 4, 5]
    y1 = [10, 12, 5, 8, 7]

    x2 = [1, 2, 3, 4, 5]
    y2 = [5, 8, 7, 2, 6]
    return (x1, y1, x2, y2)

def create_plot(predictions_line1, predictions_line2):
    plt.plot(predictions_line2, color='red', linewidth=2, linestyle='solid', label='Максимальна температура в день')
    plt.plot(predictions_line1, color='blue', linewidth=2, linestyle='solid', label='Мінімальна температура в день')
    plt.xlabel('Час')
    plt.ylabel('Температура')
    plt.title('Графік температури')
    plt.grid(True)
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf.read()

@dp.callback_query_handler(text_contains="temperature")
async def send_plot(callback_query: types.CallbackQuery):
    predictions = get_predictions()
    plot_data = create_plot(predictions[0], predictions[1])
    plot_io = io.BytesIO(plot_data)
    plot_io.name = 'plot.png'
    chat_id = callback_query.message.chat.id
    await bot.send_photo(chat_id, photo=plot_io, caption='Графік прогнозів')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
