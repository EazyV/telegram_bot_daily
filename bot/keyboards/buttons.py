"""
Keyboard for the main menu
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Получить список"), KeyboardButton("Исправить список")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
step_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Закончить"), KeyboardButton("Удалить ещё")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def create_keyboard_name_list(name_list):
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True, )
    for name in name_list:
        keyboard.add(KeyboardButton(name))
    return keyboard
