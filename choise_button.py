from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Температура", callback_data="temperature"),
            InlineKeyboardButton(text="Прогноз", callback_data="prognos"),
            ]
    ]
)