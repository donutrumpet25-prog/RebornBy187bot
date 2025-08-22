from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.navigation import back_to_main_keyboard

router = Router()

@router.message(Command("asistenta"))
async def asistenta_command(message: Message):
    # These would be configured in config.py or environment
    # For now, using placeholder usernames
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Contact Staff 1", url="https://t.me/staff1_username")],
        [InlineKeyboardButton(text="💬 Contact Staff 2", url="https://t.me/staff2_username")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    
    text = """🆘 Asistență

Ai nevoie de ajutor? Contactează echipa noastră de suport:

• Staff 1 - Pentru probleme generale
• Staff 2 - Pentru probleme tehnice

Răspundem în cel mai scurt timp posibil!"""
    
    await message.answer(text, reply_markup=keyboard)

