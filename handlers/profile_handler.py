from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.navigation import back_to_main_keyboard
from services.profile_service import ProfileService
from datetime import datetime

router = Router()

@router.message(Command("profil"))
async def profile_command(message: Message):
    profile_service = ProfileService()
    user_data = await profile_service.get_user_profile(message.from_user.id)
    
    if not user_data:
        await message.answer("Nu ai încă un profil. Folosește /start pentru a te înregistra.", 
                           reply_markup=back_to_main_keyboard())
        return
    
    # Calculate days since joining
    days_since_join = (datetime.now() - user_data.joined_at).days
    
    # Get referral count
    referral_count = await profile_service.get_referral_count(user_data.id)
    
    # Status text
    status_text = "✅ Verificat" if user_data.verified else "❌ Neverificat"
    
    # Rank names
    rank_names = ["Începător", "Inițiat", "Aspirant", "Support", "Connector", "Hustler (VIP)"]
    rank_name = rank_names[min(user_data.rank_level, len(rank_names) - 1)]
    
    text = f"""👤 Profilul tău:

📅 Vechime: {days_since_join} zile
🔰 Status: {status_text}
⚠️ Warns: {user_data.warns}/3
⚔️ Conflicte: {user_data.conflicts}
⭐ Reputație: {user_data.reputation}/5
🎯 XP Total: {user_data.xp_total}
🏆 Rank: {rank_name} (Nivel {user_data.rank_level})
🎖️ Grad: {user_data.grade or "Fără grad"}
👥 Referali calificați: {referral_count}"""

    await message.answer(text, reply_markup=back_to_main_keyboard())

@router.message(Command("info"))
async def info_command(message: Message):
    # Extract username from command
    command_parts = message.text.split()
    if len(command_parts) < 2:
        await message.answer("Folosește: /info @username", reply_markup=back_to_main_keyboard())
        return
    
    username = command_parts[1].replace("@", "")
    
    profile_service = ProfileService()
    user_data = await profile_service.get_user_by_username(username)
    
    if not user_data:
        await message.answer(f"Utilizatorul @{username} nu a fost găsit.", 
                           reply_markup=back_to_main_keyboard())
        return
    
    # Calculate days since joining
    days_since_join = (datetime.now() - user_data.joined_at).days
    
    # Get referral count
    referral_count = await profile_service.get_referral_count(user_data.id)
    
    # Status text
    status_text = "✅ Verificat" if user_data.verified else "❌ Neverificat"
    
    # Rank names
    rank_names = ["Începător", "Inițiat", "Aspirant", "Support", "Connector", "Hustler (VIP)"]
    rank_name = rank_names[min(user_data.rank_level, len(rank_names) - 1)]
    
    text = f"""👤 Profilul lui @{user_data.username}:

📅 Vechime: {days_since_join} zile
🔰 Status: {status_text}
⭐ Reputație: {user_data.reputation}/5
🎯 XP Total: {user_data.xp_total}
🏆 Rank: {rank_name} (Nivel {user_data.rank_level})
🎖️ Grad: {user_data.grade or "Fără grad"}
👥 Referali calificați: {referral_count}"""

    await message.answer(text, reply_markup=back_to_main_keyboard())

