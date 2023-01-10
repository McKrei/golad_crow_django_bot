from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


all_cur = KeyboardButton('Все валюты')
see = KeyboardButton('Слежу')
only_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(all_cur, see)
