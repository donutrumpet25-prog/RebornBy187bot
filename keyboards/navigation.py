from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def navigation_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Înapoi", callback_data="nav|to=back"),
            InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main"),
            InlineKeyboardButton(text="➡️ Înainte", callback_data="nav|to=forward")
        ]
    ])
    return keyboard

def back_to_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    return keyboard

