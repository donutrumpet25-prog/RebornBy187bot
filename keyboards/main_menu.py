from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/grup"), KeyboardButton(text="/market"), KeyboardButton(text="/locatii")],
            [KeyboardButton(text="/catalog"), KeyboardButton(text="/selleri"), KeyboardButton(text="/asistenta")],
            [KeyboardButton(text="/link"), KeyboardButton(text="/giveaway"), KeyboardButton(text="/lottery")],
            [KeyboardButton(text="/clasament"), KeyboardButton(text="/profil"), KeyboardButton(text="/ranking")],
            [KeyboardButton(text="/tutoriale"), KeyboardButton(text="/FAQ")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


