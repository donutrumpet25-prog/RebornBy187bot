from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.navigation import back_to_main_keyboard
from services.marketplace_service import MarketplaceService

router = Router()

@router.message(Command("market"))
async def market_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Locații", callback_data="market|type=locations")],
        [InlineKeyboardButton(text="📦 Catalog", callback_data="market|type=catalog")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    await message.answer("🛍️ Marketplace - Alege modul de navigare:", reply_markup=keyboard)

@router.message(Command("locatii"))
async def locations_command(message: Message):
    marketplace_service = MarketplaceService()
    locations = await marketplace_service.get_all_locations()
    
    keyboard_buttons = []
    for location in locations:
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"📍 {location.name}", 
                callback_data=f"loc|id={location.id}|p=1"
            )
        ])
    
    keyboard_buttons.append([InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await message.answer("📍 Selectează sectorul:", reply_markup=keyboard)

@router.message(Command("catalog"))
async def catalog_command(message: Message):
    marketplace_service = MarketplaceService()
    products = await marketplace_service.get_all_products()
    
    keyboard_buttons = []
    for product in products:
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"📦 {product.name}", 
                callback_data=f"prod|id={product.id}|p=1"
            )
        ])
    
    keyboard_buttons.append([InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await message.answer("📦 Selectează produsul:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("market|"))
async def market_callback(callback: CallbackQuery):
    data = callback.data.split("|")[1]
    market_type = data.split("=")[1]
    
    if market_type == "locations":
        await locations_command(callback.message)
    elif market_type == "catalog":
        await catalog_command(callback.message)
    
    await callback.answer()

@router.callback_query(F.data.startswith("loc|"))
async def location_callback(callback: CallbackQuery):
    data_parts = callback.data.split("|")
    location_id = int(data_parts[1].split("=")[1])
    page = int(data_parts[2].split("=")[1])
    
    marketplace_service = MarketplaceService()
    location = await marketplace_service.get_location_by_id(location_id)
    sellers = await marketplace_service.get_sellers_by_location(location_id, page)
    
    if not sellers:
        text = f"📍 {location.name}\n\nNu sunt selleri disponibili în acest sector."
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="market|type=locations")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    else:
        text = f"📍 {location.name}\nSelleri disponibili:"
        
        keyboard_buttons = []
        for seller in sellers:
            # Create chat link
            if seller.user.username:
                chat_url = f"https://t.me/{seller.user.username}"
            else:
                chat_url = f"tg://user?id={seller.user.tg_id}"
            
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text=f"💬 {seller.display_name or seller.user.first_name}",
                    url=chat_url
                )
            ])
        
        # Navigation buttons
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"loc|id={location_id}|p={page-1}"))
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Înapoi", callback_data="market|type=locations"))
        nav_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"loc|id={location_id}|p={page+1}"))
        
        keyboard_buttons.append(nav_buttons)
        keyboard_buttons.append([InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("prod|"))
async def product_callback(callback: CallbackQuery):
    data_parts = callback.data.split("|")
    product_id = int(data_parts[1].split("=")[1])
    page = int(data_parts[2].split("=")[1])
    
    marketplace_service = MarketplaceService()
    product = await marketplace_service.get_product_by_id(product_id)
    sellers = await marketplace_service.get_sellers_by_product(product_id, page)
    
    text = f"🛍️ {product.name}"
    if product.description:
        text += f"\n{product.description}"
    
    if not sellers:
        text += "\n\nNu sunt selleri disponibili pentru acest produs."
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="market|type=catalog")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    else:
        text += "\n\nSelleri disponibili:"
        
        keyboard_buttons = []
        for seller in sellers:
            # Create chat link
            if seller.user.username:
                chat_url = f"https://t.me/{seller.user.username}"
            else:
                chat_url = f"tg://user?id={seller.user.tg_id}"
            
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text=f"💬 {seller.display_name or seller.user.first_name}",
                    url=chat_url
                )
            ])
        
        # Navigation buttons
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"prod|id={product_id}|p={page-1}"))
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Înapoi", callback_data="market|type=catalog"))
        nav_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"prod|id={product_id}|p={page+1}"))
        
        keyboard_buttons.append(nav_buttons)
        keyboard_buttons.append([InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

