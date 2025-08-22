from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.main_menu import main_menu_keyboard

router = Router()

@router.callback_query(F.data.startswith("nav|"))
async def navigation_callback(callback: CallbackQuery):
    data = callback.data.split("|")[1]
    action = data.split("=")[1]
    
    if action == "main":
        # Go to main menu
        text = f"🏠 Meniu Principal\n\nSalut, @{callback.from_user.username}! Selectează o opțiune:"
        await callback.message.edit_text(text, reply_markup=main_menu_keyboard())
    
    elif action == "back":
        # This would need context to know where to go back
        # For now, just go to main menu
        text = f"🏠 Meniu Principal\n\nSalut, @{callback.from_user.username}! Selectează o opțiune:"
        await callback.message.edit_text(text, reply_markup=main_menu_keyboard())
    
    elif action == "forward":
        # This would need context to know where to go forward
        # For now, just show a message
        await callback.answer("Nu există o pagină următoare.", show_alert=True)
        return
    
    await callback.answer()

