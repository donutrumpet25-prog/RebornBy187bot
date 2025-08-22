from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.navigation import back_to_main_keyboard

router = Router()

@router.message(Command("giveaway"))
async def giveaway_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Giveaway-uri active", callback_data="gw|action=list")],
        [InlineKeyboardButton(text="📋 Reguli", callback_data="gw|action=rules")],
        [InlineKeyboardButton(text="🏆 Extrageri", callback_data="gw|action=draws")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    
    await message.answer("🎁 Giveaway - Selectează o opțiune:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("gw|"))
async def giveaway_callback(callback: CallbackQuery):
    data = callback.data.split("|")[1]
    action = data.split("=")[1]
    
    if action == "list":
        text = """🎁 Giveaway-uri Active

📅 Momentan nu sunt giveaway-uri active.

Urmărește anunțurile din grup pentru a afla când vor fi lansate noi giveaway-uri!"""
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Actualizează", callback_data="gw|action=list")],
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="gw|back=main")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    
    elif action == "rules":
        text = """📋 Reguli Giveaway

🎯 Condiții de participare:
• Să fii membru al grupului oficial
• Să ai profilul verificat (pentru premii mari)
• Să nu ai warns active
• Să respecti regulile comunității

🏆 Tipuri de premii:
• Crypto (BTC, LTC, ETH)
• Produse din marketplace
• Rank-uri speciale
• XP bonus

⚠️ Restricții:
• O singură participare per giveaway
• Conturile fake sunt descalificate
• Premiile expiră în 7 zile dacă nu sunt revendicate"""
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="gw|back=main")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    
    elif action == "draws":
        text = """🏆 Extrageri Recente

📅 Nu au fost încă extrageri.

Istoricul extragerilor va apărea aici după primul giveaway."""
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Actualizează", callback_data="gw|action=draws")],
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="gw|back=main")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "gw|back=main")
async def giveaway_back(callback: CallbackQuery):
    await giveaway_command(callback.message)

