from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.main_menu import main_menu_keyboard
from services.profile_service import ProfileService
from services.referral_service import ReferralService

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message):
    profile_service = ProfileService()
    
    # Create or update user profile
    user = await profile_service.create_or_update_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )
    
    # Check if this is a referral start
    command_args = message.text.split()
    if len(command_args) > 1 and command_args[1].startswith("ref_"):
        referral_code = command_args[1]
        referral_service = ReferralService()
        await referral_service.process_referral(referral_code, message.from_user.id)
    
    await message.answer(
        f"Salut, @{message.from_user.username}! Bine ai venit pe RebornBy187bot.\n"
        "• Vezi comenzile cu /help\n"
        "• Învață rapid cu /tutoriale\n"
        "• Cumpără din /market (după sector sau produs)\n"
        "• Crește cu /link (referral), adună XP, urcă în /ranking și /clasament",
        reply_markup=main_menu_keyboard()
    )


