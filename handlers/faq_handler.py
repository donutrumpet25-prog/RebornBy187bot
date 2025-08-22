from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.navigation import back_to_main_keyboard

router = Router()

@router.message(Command("FAQ"))
async def faq_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 XP & Ranking", callback_data="faq|topic=xp")],
        [InlineKeyboardButton(text="👥 Referral", callback_data="faq|topic=referral")],
        [InlineKeyboardButton(text="📋 Comenzi & Status", callback_data="faq|topic=commands")],
        [InlineKeyboardButton(text="🔒 Securitate", callback_data="faq|topic=security")],
        [InlineKeyboardButton(text="🛍️ Marketplace", callback_data="faq|topic=marketplace")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    await message.answer("❓ Întrebări frecvente - Selectează o categorie:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("faq|"))
async def faq_callback(callback: CallbackQuery):
    data = callback.data.split("|")[1]
    topic = data.split("=")[1]
    
    if topic == "xp":
        text = """🎯 XP & Ranking

❓ Cum se calculează XP-ul?
• +100 XP pentru fiecare referral calificat
• +10 XP săptămânal pentru vechime
• +25 XP pentru fiecare comandă confirmată
• +100 XP pentru Verificare FULL

❓ Când se actualizează ranking-ul?
• Automat la fiecare acțiune care acordă XP
• Săptămânal pentru XP-ul de vechime

❓ Care sunt pragurile de rank?
• 15 referali → Inițiat
• 20 referali → Aspirant
• 25 referali → Support
• 50 referali → Connector
• 100+ referali → Hustler (VIP)"""
    
    elif topic == "referral":
        text = """👥 Referral

❓ Cum funcționează sistemul de referral?
• Generezi un link unic cu /link
• Persoanele care se înscriu prin linkul tău devin referalii tăi
• Primești +100 XP când referalul devine calificat

❓ Când devine un referral calificat?
• Când persoana invitată se alătură botului ȘI grupului oficial

❓ Condiții pentru link referral:
• Trebuie să fii membru al grupului oficial
• Un user poate fi invitat o singură dată
• Nu poți să te auto-inviți"""
    
    elif topic == "commands":
        text = """📋 Comenzi & Status

❓ Ce înseamnă "Verificat"?
• Status acordat manual de admin
• Oferă +100 XP bonus
• Indică încredere sporită în comunitate

❓ Ce sunt warns-urile?
• Avertismente acordate de admin
• Maxim 3 warns per user
• La 3 warns poți fi restricționat

❓ Comenzi principale:
• /start - Meniu principal
• /profil - Vezi statisticile tale
• /market - Accesează marketplace-ul
• /link - Generează link referral"""
    
    elif topic == "security":
        text = """🔒 Securitate

❓ Anti-abuz referral:
• Nu poți să te auto-inviți
• Un user poate fi invitat o singură dată
• Conturile care pleacă imediat sunt marcate rejected

❓ Warns 0/3:
• Sistem de avertismente
• Acordate manual de admin
• La 3 warns riști restricții

❓ Conflicte:
• Înregistrează disputele cu alți useri
• Afectează reputația
• Monitorizate de admin"""
    
    elif topic == "marketplace":
        text = """🛍️ Marketplace

❓ Cum cumpăr ceva?
• Folosește /market pentru a naviga
• Selectează după locație (/locatii) sau produs (/catalog)
• Apasă pe butonul sellerului pentru chat direct

❓ Cum contactez un seller?
• Din orice listă de selleri, apasă pe numele lui
• Se va deschide chat direct cu sellerul
• Poți negocia direct cu el

❓ Cum devin seller?
• Contactează un admin
• Adminul te va adăuga cu /add_seller
• Vei apărea în toate listele relevante"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Înapoi la FAQ", callback_data="faq|back=main")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "faq|back=main")
async def faq_back(callback: CallbackQuery):
    await faq_command(callback.message)

