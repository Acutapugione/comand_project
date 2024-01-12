from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Прогноз погоди на сьогодні", callback_data="prognos_todey"),
            InlineKeyboardButton(text="Прогноз погоди де я живу", callback_data="prognos_id"),
            InlineKeyboardButton(text="Прогноз погоди на 7 днів вперед", callback_data="prognos_forecast_days"),
            ]
    ]
)

start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Прогноз погоди де я живу", callback_data="prognos_id"),
            ]
    ]
)

todey_id = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад до меню", callback_data="back_to_menu"),
            ]
    ]
)

f_d_p = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back_1"),
            InlineKeyboardButton(text="Далі", callback_data="further_1"),
            InlineKeyboardButton(text="Назад до меню", callback_data="back_to_menu"),
            ]
    ]
)

f_d_t = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back_2"),
            InlineKeyboardButton(text="Далі", callback_data="further_2"),
            InlineKeyboardButton(text="Назад до меню", callback_data="back_to_menu"),
            ]
    ]
)

f_d_w_s = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back_3"),
            InlineKeyboardButton(text="Далі", callback_data="further_3"),
            InlineKeyboardButton(text="Назад до меню", callback_data="back_to_menu"),
            ]
    ]
)

f_d_w_d = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back_4"),
            InlineKeyboardButton(text="Далі", callback_data="further_4"),
            InlineKeyboardButton(text="Назад до меню", callback_data="back_to_menu"),
            ]
    ]
)

f_d_pr = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back_5"),
            InlineKeyboardButton(text="Далі", callback_data="further_5"),
            InlineKeyboardButton(text="Назад до меню", callback_data="back_to_menu"),
            ]
    ]
)