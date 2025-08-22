from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.navigation import back_to_main_keyboard
from services.referral_service import ReferralService
from services.membership_service import MembershipService

router = Router()

@router.message(Command("link"))
async def link_command(message: Message):
    referral_service = ReferralService()
    membership_service = MembershipService()
    
    # Check if user is in group
    is_member = await membership_service.check_group_membership(message.from_user.id)
    
    if not is_member:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Intră în grup", callback_data="ref|action=join_group")],
            [InlineKeyboardButton(text="✅ Am intrat", callback_data="ref|action=check_join")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
        text = """🔗 Link Referral

Pentru a primi linkul tău personal, intră în grupul oficial.

După ce intri în grup, apasă "Am intrat" pentru a verifica."""
    else:
        # User is in group, generate/show referral link
        referral_code = await referral_service.get_or_create_referral_code(message.from_user.id)
        referral_link = f"https://t.me/RebornBy187bot?start={referral_code}"
        
        # Get referral stats
        stats = await referral_service.get_referral_stats(message.from_user.id)
        
        text = f"""🔗 Linkul tău unic:

{referral_link}

📊 Statistici:
• Invitați total: {stats['total']}
• Calificați: {stats['qualified']}
• În așteptare: {stats['pending']}

💡 Un referral devine calificat când persoana invitată se alătură botului ȘI grupului oficial."""
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Actualizează", callback_data="ref|action=refresh")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data.startswith("ref|"))
async def referral_callback(callback: CallbackQuery):
    data = callback.data.split("|")[1]
    action = data.split("=")[1]
    
    referral_service = ReferralService()
    membership_service = MembershipService()
    
    if action == "join_group":
        # This would open the group link - for now just show message
        await callback.answer("Deschide linkul grupului din meniul principal (/grup)", show_alert=True)
    
    elif action == "check_join":
        # Check if user joined the group
        is_member = await membership_service.check_group_membership(callback.from_user.id)
        
        if is_member:
            # Update user's group status
            await membership_service.update_group_status(callback.from_user.id, True)
            
            # Generate referral link
            referral_code = await referral_service.get_or_create_referral_code(callback.from_user.id)
            referral_link = f"https://t.me/RebornBy187bot?start={referral_code}"
            
            # Get referral stats
            stats = await referral_service.get_referral_stats(callback.from_user.id)
            
            text = f"""✅ Felicitări! Ești membru al grupului.

🔗 Linkul tău unic:
{referral_link}

📊 Statistici:
• Invitați total: {stats['total']}
• Calificați: {stats['qualified']}
• În așteptare: {stats['pending']}"""
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Actualizează", callback_data="ref|action=refresh")],
                [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
            ])
        else:
            text = """❌ Nu ești încă membru al grupului.

Te rugăm să intri în grupul oficial și apoi să apeși din nou "Am intrat"."""
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔗 Intră în grup", callback_data="ref|action=join_group")],
                [InlineKeyboardButton(text="✅ Am intrat", callback_data="ref|action=check_join")],
                [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
            ])
        
        await callback.message.edit_text(text, reply_markup=keyboard)
    
    elif action == "refresh":
        # Refresh referral stats
        stats = await referral_service.get_referral_stats(callback.from_user.id)
        referral_code = await referral_service.get_or_create_referral_code(callback.from_user.id)
        referral_link = f"https://t.me/RebornBy187bot?start={referral_code}"
        
        text = f"""🔗 Linkul tău unic:

{referral_link}

📊 Statistici actualizate:
• Invitați total: {stats['total']}
• Calificați: {stats['qualified']}
• În așteptare: {stats['pending']}

💡 Un referral devine calificat când persoana invitată se alătură botului ȘI grupului oficial."""
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Actualizează", callback_data="ref|action=refresh")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard)
    
    await callback.answer()

