from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.navigation import back_to_main_keyboard

router = Router()

@router.message(Command("tutoriale"))
async def tutoriale_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 LTC din Revolut", callback_data="tut|topic=revolut")],
        [InlineKeyboardButton(text="🏧 Plată ATM Crypto", callback_data="tut|topic=atm")],
        [InlineKeyboardButton(text="🍰 Cake Wallet", callback_data="tut|topic=cake")],
        [InlineKeyboardButton(text="🤖 Cum funcționează platforma", callback_data="tut|topic=platform")],
        [InlineKeyboardButton(text="📝 Abrevieri", callback_data="tut|topic=abbrev")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    await message.answer("📚 Tutoriale - Selectează un subiect:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("tut|"))
async def tutorial_callback(callback: CallbackQuery):
    data = callback.data.split("|")[1]
    topic = data.split("=")[1]
    
    if topic == "revolut":
        text = """💰 Cum cumperi și transferi LTC din Revolut

1️⃣ Deschide aplicația Revolut
2️⃣ Mergi la secțiunea "Crypto"
3️⃣ Caută "Litecoin (LTC)"
4️⃣ Apasă "Buy" și introdu suma dorită
5️⃣ Confirmă tranzacția
6️⃣ Pentru transfer:
   • Apasă pe LTC din portofoliu
   • Selectează "Send"
   • Introdu adresa wallet-ului destinație
   • Confirmă transferul

⚠️ Atenție: Verifică întotdeauna adresa de destinație!"""
    
    elif topic == "atm":
        text = """🏧 Cum faci o plată de la ATM Crypto

1️⃣ Găsește un ATM crypto în apropiere
2️⃣ Selectează "Buy Cryptocurrency"
3️⃣ Alege moneda dorită (BTC, LTC, etc.)
4️⃣ Introdu suma în lei
5️⃣ Scanează QR code-ul wallet-ului tău
6️⃣ Introdu banii cash în ATM
7️⃣ Confirmă tranzacția
8️⃣ Așteaptă confirmarea pe blockchain

💡 Tip: Ai nevoie de un wallet crypto pentru a primi monedele!"""
    
    elif topic == "cake":
        text = """🍰 Cake Wallet (Fast & Safe)

📱 Instalare:
• Descarcă din App Store/Google Play
• Verifică că este aplicația oficială

🔐 Setup:
1️⃣ Creează un wallet nou
2️⃣ Salvează seed phrase-ul (12-24 cuvinte)
3️⃣ Setează un PIN puternic
4️⃣ Activează autentificarea biometrică

💸 Utilizare:
• "Receive" - pentru a primi crypto
• "Send" - pentru a trimite crypto
• "Exchange" - pentru a schimba între monede

🛡️ Securitate: Nu împărtăși niciodată seed phrase-ul!"""
    
    elif topic == "platform":
        text = """🤖 Cum funcționează platforma

🏪 Marketplace:
• /market - Accesează marketplace-ul
• /locatii - Caută selleri pe sectoare
• /catalog - Caută produse specifice
• /selleri - Vezi toți sellerii

👥 Referral:
• /link - Generează linkul tău unic
• Invită prieteni și primești XP
• Urcă în clasament cu /clasament

🎯 Progres:
• /profil - Vezi statisticile tale
• /ranking - Vezi progresul către următorul nivel
• Câștigă XP din referali și comenzi

💬 Suport:
• /asistenta - Contact direct cu staff-ul
• /grup - Alătură-te grupului oficial"""
    
    elif topic == "abbrev":
        text = """📝 Abrevieri comune

💰 Crypto:
• BTC - Bitcoin
• LTC - Litecoin
• ETH - Ethereum
• USDT - Tether

🏪 Marketplace:
• S1-S6 - Sectoarele 1-6 București
• XP - Experience Points
• VIP - Hustler rank (100+ referali)

👤 Roluri:
• Admin - Administrator
• Staff - Membru staff
• Seller - Vânzător verificat
• User - Utilizator normal

📊 Status:
• Verificat - Cont verificat de admin
• Warns - Avertismente (max 3)
• Rep - Reputație (1-5 stele)"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Înapoi la Tutoriale", callback_data="tut|back=main")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "tut|back=main")
async def tutorial_back(callback: CallbackQuery):
    await tutoriale_command(callback.message)

