from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.navigation import navigation_keyboard

router = Router()

@router.message(Command("help"))
async def help_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="User", callback_data="help|role=user")],
        [InlineKeyboardButton(text="Seller", callback_data="help|role=seller")],
        [InlineKeyboardButton(text="Admin", callback_data="help|role=admin")]
    ])
    await message.answer("Selectează rolul pentru a vedea comenzile disponibile:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("help|"))
async def help_callback(callback: CallbackQuery):
    data = callback.data.split("|")[1]
    role = data.split("=")[1]
    
    if role == "user":
        text = """🔹 Comenzi User:
/start - Meniu principal
/profil - Vezi profilul tău
/info @user - Vezi profilul unui user
/market - Marketplace (locații și catalog)
/locatii - Vezi selleri pe sectoare
/catalog - Vezi produse disponibile
/selleri - Index complet selleri
/link - Generează link referral
/clasament - Leaderboard
/ranking - Vezi progresul tău
/asistenta - Contact staff
/grup - Link grup oficial
/giveaway - Participă la giveaway
/lottery - Participă la lottery
/tutoriale - Învață să folosești platforma
/FAQ - Întrebări frecvente"""
    
    elif role == "seller":
        text = """🔹 Comenzi Seller (toate comenzile User +):
• Apari în listele de selleri
• Poți fi contactat direct din bot
• Ai reputație și poți avea produse + sector(e)"""
    
    elif role == "admin":
        text = """🔹 Comenzi Admin:
/add_seller @user - Adaugă seller
/remove_seller @user - Elimină seller
/set_location @user <sector> - Setează locația sellerului
/set_product @user <prod1,prod2> - Setează produse seller
/remove_product @user <prod> - Elimină produs seller
/add_product <nume> [descriere] - Adaugă produs global
/remove_product <prod> - Elimină produs global
/add_location <nume|sector> - Adaugă locație
/remove_location <id> - Elimină locație
/give_rank @user <nivel> - Acordă rank
/give_grad @user <grad> - Acordă grad
/confirm_order <txn_id> - Confirmă tranzacție
/launch_giveaway - Lansează giveaway
/draw_giveaway - Extrage câștigători
/launch_lottery - Lansează lottery
/draw_lottery - Extrage câștigători"""
    
    await callback.message.edit_text(text, reply_markup=navigation_keyboard())
    await callback.answer()

