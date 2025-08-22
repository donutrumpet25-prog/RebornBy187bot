from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.navigation import back_to_main_keyboard
from services.clasament_service import ClasamentService

router = Router()

@router.message(Command("clasament"))
async def clasament_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 All-time", callback_data="lb|range=all|p=1")],
        [InlineKeyboardButton(text="📅 Top 30 zile", callback_data="lb|range=30|p=1")],
        [InlineKeyboardButton(text="⚡ Top 7 zile", callback_data="lb|range=7|p=1")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    await message.answer("🏆 Clasament - Selectează perioada:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("lb|"))
async def leaderboard_callback(callback: CallbackQuery):
    data_parts = callback.data.split("|")
    range_type = data_parts[1].split("=")[1]
    page = int(data_parts[2].split("=")[1])
    
    clasament_service = ClasamentService()
    
    # Get leaderboard data
    leaderboard = await clasament_service.get_leaderboard(range_type, page)
    user_position = await clasament_service.get_user_position(callback.from_user.id, range_type)
    
    if not leaderboard:
        text = f"🏆 Clasament {range_type}\n\nNu sunt date disponibile."
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="lb|back=main")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    else:
        # Format range text
        if range_type == "all":
            range_text = "All-time"
        elif range_type == "30":
            range_text = "Top 30 zile"
        elif range_type == "7":
            range_text = "Top 7 zile"
        
        text = f"🏆 Clasament {range_text}\n\n"
        
        # Add leaderboard entries
        start_position = (page - 1) * 10 + 1
        for i, entry in enumerate(leaderboard):
            position = start_position + i
            username = entry['username'] or "User"
            refs = entry['qualified_referrals']
            xp = entry['xp_total']
            
            if position == 1:
                emoji = "🥇"
            elif position == 2:
                emoji = "🥈"
            elif position == 3:
                emoji = "🥉"
            else:
                emoji = f"{position})"
            
            text += f"{emoji} @{username} — {refs} ref | {xp} XP\n"
        
        # Add user position
        if user_position:
            text += f"\n📍 Tu ești pe locul {user_position}."
        
        # Navigation buttons
        keyboard_buttons = []
        nav_buttons = []
        
        if page > 1:
            nav_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"lb|range={range_type}|p={page-1}"))
        
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Înapoi", callback_data="lb|back=main"))
        
        if len(leaderboard) == 10:  # Full page, might have more
            nav_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"lb|range={range_type}|p={page+1}"))
        
        keyboard_buttons.append(nav_buttons)
        keyboard_buttons.append([InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "lb|back=main")
async def leaderboard_back(callback: CallbackQuery):
    await clasament_command(callback.message)

