from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton('🔎 Поиск'))
    keyboard.add(KeyboardButton('🌎 Выбрать регион'))
    keyboard.add(KeyboardButton('🗒 Показать результаты'))
    keyboard.add(KeyboardButton('❌ Сброс поиска'))
    return keyboard


def cities_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('Весь Узбекистан')
    keyboard.add('Ташкент')
    keyboard.add('Самарканд')
    return keyboard

