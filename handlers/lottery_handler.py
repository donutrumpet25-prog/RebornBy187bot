from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.navigation import back_to_main_keyboard

router = Router()

@router.message(Command("lottery"))
async def lottery_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Participă", callback_data="lot|action=join")],
        [InlineKeyboardButton(text="📋 Reguli", callback_data="lot|action=rules")],
        [InlineKeyboardButton(text="📊 Istoric", callback_data="lot|action=history")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    
    await message.answer("🎲 Lottery - Selectează o opțiune:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("lot|"))
async def lottery_callback(callback: CallbackQuery):
    data = callback.data.split("|")[1]
    action = data.split("=")[1]
    
    if action == "join":
        text = """🎲 Participă la Lottery

📅 Următoarea tragere: În curând

💰 Premiul curent: Se anunță

🎯 Pentru a participa:
• Fii membru activ al grupului
• Ai minim 10 XP
• Nu ai warns active

⏰ Tragerile se fac săptămânal, duminica la 20:00."""
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Înscrie-mă", callback_data="lot|action=register")],
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="lot|back=main")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    
    elif action == "rules":
        text = """📋 Reguli Lottery

🎯 Condiții de participare:
• Membru al grupului oficial
• Minim 10 XP în cont
• Fără warns active
• Activitate recentă în comunitate

🎲 Cum funcționează:
• Trageri săptămânale (duminica, 20:00)
• Participarea este gratuită
• Un câștigător per tragere
• Premiile variază săptămânal

💰 Tipuri de premii:
• Crypto (BTC, LTC)
• XP bonus (500-1000)
• Rank upgrade temporar
• Produse din marketplace

⚠️ Restricții:
• Maxim o participare per săptămână
• Câștigătorii nu pot participa următoarele 2 săptămâni
• Premiile expiră în 48h dacă nu sunt revendicate"""
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="lot|back=main")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    
    elif action == "history":
        text = """📊 Istoric Lottery

🏆 Câștigători recenți:

📅 Nu au fost încă trageri.

Istoricul va fi actualizat după prima tragere."""
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Actualizează", callback_data="lot|action=history")],
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="lot|back=main")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    
    elif action == "register":
        # This would check eligibility and register the user
        text = """✅ Înregistrare Lottery

🎉 Te-ai înscris cu succes la următoarea tragere!

📅 Tragerea va avea loc duminica la 20:00
🍀 Mult noroc!

Vei fi notificat dacă câștigi."""
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="lot|back=main")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "lot|back=main")
async def lottery_back(callback: CallbackQuery):
    await lottery_command(callback.message)

