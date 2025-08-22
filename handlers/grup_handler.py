from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.navigation import back_to_main_keyboard

router = Router()

@router.message(Command("grup"))
async def grup_command(message: Message):
    # This would be configured in config.py
    # For now, using placeholder group link
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Intră în grup", url="https://t.me/rebornby187_group")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    
    text = """👥 Grupul Oficial

Alătură-te comunității noastre pentru:

• Discuții în timp real
• Anunțuri importante
• Suport din partea comunității
• Oportunități exclusive

Pentru a primi link-ul de referral, trebuie să fii membru al grupului!"""
    
    await message.answer(text, reply_markup=keyboard)

