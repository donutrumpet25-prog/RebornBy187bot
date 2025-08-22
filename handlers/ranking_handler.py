from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.navigation import back_to_main_keyboard
from services.ranking_service import RankingService

router = Router()

@router.message(Command("ranking"))
async def ranking_command(message: Message):
    ranking_service = RankingService()
    user_progress = await ranking_service.get_user_progress(message.from_user.id)
    
    if not user_progress:
        await message.answer("Nu ai încă un profil. Folosește /start pentru a te înregistra.", 
                           reply_markup=back_to_main_keyboard())
        return
    
    # Rank names and thresholds
    rank_info = [
        {"name": "Începător", "threshold": 0},
        {"name": "Inițiat", "threshold": 15},
        {"name": "Aspirant", "threshold": 20},
        {"name": "Support", "threshold": 25},
        {"name": "Connector", "threshold": 50},
        {"name": "Hustler (VIP)", "threshold": 100}
    ]
    
    current_rank = rank_info[min(user_progress['rank_level'], len(rank_info) - 1)]
    qualified_refs = user_progress['qualified_referrals']
    
    # Calculate progress to next rank
    if user_progress['rank_level'] < len(rank_info) - 1:
        next_rank = rank_info[user_progress['rank_level'] + 1]
        progress = qualified_refs - current_rank['threshold']
        needed = next_rank['threshold'] - current_rank['threshold']
        progress_percent = min(100, (progress / needed) * 100) if needed > 0 else 100
        
        # Create progress bar
        filled_blocks = int(progress_percent / 10)
        empty_blocks = 10 - filled_blocks
        progress_bar = "█" * filled_blocks + "░" * empty_blocks
        
        next_rank_text = f"""
🎯 Progres către {next_rank['name']}:
{progress_bar} {progress_percent:.1f}%
{qualified_refs}/{next_rank['threshold']} referali calificați
Mai ai nevoie de {next_rank['threshold'] - qualified_refs} referali"""
    else:
        next_rank_text = "\n🏆 Ai atins rankul maxim!"
    
    text = f"""🏆 Ranking & Progres

📊 Statusul tău actual:
• Rank: {current_rank['name']} (Nivel {user_progress['rank_level']})
• Referali calificați: {qualified_refs}
• XP Total: {user_progress['xp_total']}
• Grad: {user_progress['grade'] or 'Fără grad'}

{next_rank_text}

📋 Praguri ranking (după #referali calificați):
• 15 → Inițiat
• 20 → Aspirant  
• 25 → Support
• 50 → Connector
• 100+ → Hustler (VIP)

💡 Gradele sunt acordate manual de admin și reprezintă roluri speciale în comunitate."""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Vezi clasamentul", callback_data="ranking|action=leaderboard")],
        [InlineKeyboardButton(text="🔄 Actualizează", callback_data="ranking|action=refresh")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data.startswith("ranking|"))
async def ranking_callback(callback: CallbackQuery):
    data = callback.data.split("|")[1]
    action = data.split("=")[1]
    
    if action == "refresh":
        await ranking_command(callback.message)
    elif action == "leaderboard":
        # Redirect to clasament command
        from handlers.clasament_handler import clasament_command
        await clasament_command(callback.message)
    
    await callback.answer()

