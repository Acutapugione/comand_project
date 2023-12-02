import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram import executor
import matplotlib.pyplot as plt
import io


with open('settings.json') as _file:
    settings = json.load(_file)

token = settings.get('bot').get('token')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_predictions(message: types.Message):
    await message.answer(f'Привіт. Я бот який покаже тобі прогноз погоди на ближайший тиждень. Подивись прогноз погоди на тиждень нажав на кнопку "Прогноз"')

def get_predictions():
    return [1, 2, 3, 4, 5]

@dp.message_handler(commands=['predictions'])
async def send_predictions(message: types.Message):
    predictions = get_predictions()
    await message.answer(f'Прогнози: {predictions}')

def create_plot(predictions):
    plt.plot(predictions)
    plt.xlabel('Час')
    plt.ylabel('Прогнози')
    plt.title('Графік прогнозів')
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf.read()


@dp.message_handler(commands=['plot'])
async def send_plot(message: types.Message):
    predictions = get_predictions()
    plot_data = create_plot(predictions)
    plot_io = io.BytesIO(plot_data)
    plot_io.name = 'plot.png'
    await bot.send_photo(message.chat.id, photo=plot_io, caption='Графік прогнозів')


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
