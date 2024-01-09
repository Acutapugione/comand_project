from choise_button import choice, start
from config import bot_token
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types


dp = Router()

class WeatherState(StatesGroup):
    city = State()

@dp.message(CommandStart())
async def send_predictions(message: types.Message, state: FSMContext):
    await message.answer(text='Привіт. Я бот, який покаже тобі погоду на день і місто, яке ти вибереш. Введи місто:', reply_markup=start)
    await state.set_state(WeatherState.city)

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_1(message: types.Message, state: FSMContext):
    await message.message.answer(text='Напиши нове місто:', reply_markup=start)
    await state.set_state(WeatherState.city)

@dp.message(WeatherState.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.clear()
    await state.update_data(city=message.text)
    await message.reply('Виберіть на який день чи тиждень ви хочете подивитися погоду:', reply_markup=choice)


async def main():
    bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher()
    dispatcher.include_router(dp)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    