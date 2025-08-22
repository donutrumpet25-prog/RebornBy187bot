from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.navigation import back_to_main_keyboard
from services.marketplace_service import MarketplaceService

router = Router()

@router.message(Command("selleri"))
async def sellers_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Toți selleri", callback_data="sellers|type=all|p=1")],
        [InlineKeyboardButton(text="📍 Selleri pe sectoare", callback_data="sellers|type=sectors")],
        [InlineKeyboardButton(text="🔍 Filtre", callback_data="sellers|type=filters")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    await message.answer("👥 Selleri - Selectează modul de vizualizare:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("sellers|"))
async def sellers_callback(callback: CallbackQuery):
    data_parts = callback.data.split("|")
    seller_type = data_parts[1].split("=")[1]
    
    marketplace_service = MarketplaceService()
    
    if seller_type == "all":
        page = int(data_parts[2].split("=")[1])
        sellers = await marketplace_service.get_all_sellers(page)
        
        if not sellers:
            text = "👥 Nu sunt selleri disponibili."
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
            ])
        else:
            text = "👥 Toți sellerii:\n\n"
            
            keyboard_buttons = []
            for seller in sellers:
                # Create seller info text
                location_text = f" - {seller.location.name}" if seller.location else ""
                seller_text = f"👤 {seller.display_name or seller.user.first_name}{location_text}"
                
                # Create chat link
                if seller.user.username:
                    chat_url = f"https://t.me/{seller.user.username}"
                else:
                    chat_url = f"tg://user?id={seller.user.tg_id}"
                
                keyboard_buttons.append([
                    InlineKeyboardButton(text=seller_text, callback_data=f"seller|id={seller.id}"),
                    InlineKeyboardButton(text="💬 Chat", url=chat_url)
                ])
            
            # Navigation buttons
            nav_buttons = []
            if page > 1:
                nav_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"sellers|type=all|p={page-1}"))
            nav_buttons.append(InlineKeyboardButton(text="⬅️ Înapoi", callback_data="sellers|back=main"))
            nav_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"sellers|type=all|p={page+1}"))
            
            keyboard_buttons.append(nav_buttons)
            keyboard_buttons.append([InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    elif seller_type == "sectors":
        keyboard_buttons = []
        for i in range(1, 7):
            keyboard_buttons.append([
                InlineKeyboardButton(text=f"📍 Sector {i}", callback_data=f"sellers|sector={i}|p=1")
            ])
        
        keyboard_buttons.append([InlineKeyboardButton(text="⬅️ Înapoi", callback_data="sellers|back=main")])
        keyboard_buttons.append([InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        text = "📍 Selectează sectorul:"
    
    elif seller_type == "filters":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📍 După sector", callback_data="filter|type=sector")],
            [InlineKeyboardButton(text="📦 După produs", callback_data="filter|type=product")],
            [InlineKeyboardButton(text="⭐ După reputație", callback_data="filter|type=reputation")],
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="sellers|back=main")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
        text = "🔍 Selectează tipul de filtru:"
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("sellers|sector="))
async def sellers_sector_callback(callback: CallbackQuery):
    data_parts = callback.data.split("|")
    sector = int(data_parts[1].split("=")[1])
    page = int(data_parts[2].split("=")[1])
    
    marketplace_service = MarketplaceService()
    sellers = await marketplace_service.get_sellers_by_sector(sector, page)
    
    if not sellers:
        text = f"📍 Sector {sector}\n\nNu sunt selleri disponibili în acest sector."
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="sellers|type=sectors")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    else:
        text = f"📍 Sector {sector} - Selleri disponibili:\n\n"
        
        keyboard_buttons = []
        for seller in sellers:
            # Create seller info text
            seller_text = f"👤 {seller.display_name or seller.user.first_name} ⭐{seller.reputation}"
            
            # Create chat link
            if seller.user.username:
                chat_url = f"https://t.me/{seller.user.username}"
            else:
                chat_url = f"tg://user?id={seller.user.tg_id}"
            
            keyboard_buttons.append([
                InlineKeyboardButton(text=seller_text, callback_data=f"seller|id={seller.id}"),
                InlineKeyboardButton(text="💬 Chat", url=chat_url)
            ])
        
        # Navigation buttons
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"sellers|sector={sector}|p={page-1}"))
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Înapoi", callback_data="sellers|type=sectors"))
        nav_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"sellers|sector={sector}|p={page+1}"))
        
        keyboard_buttons.append(nav_buttons)
        keyboard_buttons.append([InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "sellers|back=main")
async def sellers_back(callback: CallbackQuery):
    await sellers_command(callback.message)

@router.callback_query(F.data.startswith("seller|"))
async def seller_info_callback(callback: CallbackQuery):
    data_parts = callback.data.split("|")
    seller_id = int(data_parts[1].split("=")[1])
    
    # Get seller details (this would need a service method)
    # For now, just show a placeholder
    text = f"👤 Informații seller #{seller_id}\n\n(Detalii seller vor fi implementate)"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="sellers|type=all|p=1")],
        [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("filter|"))
async def filter_callback(callback: CallbackQuery):
    data_parts = callback.data.split("|")
    filter_type = data_parts[1].split("=")[1]
    
    if filter_type == "sector":
        keyboard_buttons = []
        for i in range(1, 7):
            keyboard_buttons.append([
                InlineKeyboardButton(text=f"📍 Sector {i}", callback_data=f"filter|sector={i}|p=1")
            ])
        
        keyboard_buttons.append([InlineKeyboardButton(text="⬅️ Înapoi", callback_data="sellers|type=filters")])
        keyboard_buttons.append([InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        text = "📍 Filtrează după sector:"
    
    elif filter_type == "product":
        marketplace_service = MarketplaceService()
        products = await marketplace_service.get_all_products()
        
        keyboard_buttons = []
        for product in products:
            keyboard_buttons.append([
                InlineKeyboardButton(text=f"📦 {product.name}", callback_data=f"filter|prod={product.id}|p=1")
            ])
        
        keyboard_buttons.append([InlineKeyboardButton(text="⬅️ Înapoi", callback_data="sellers|type=filters")])
        keyboard_buttons.append([InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        text = "📦 Filtrează după produs:"
    
    elif filter_type == "reputation":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⭐ 1+ stele", callback_data="filter|rep=1|p=1")],
            [InlineKeyboardButton(text="⭐⭐ 2+ stele", callback_data="filter|rep=2|p=1")],
            [InlineKeyboardButton(text="⭐⭐⭐ 3+ stele", callback_data="filter|rep=3|p=1")],
            [InlineKeyboardButton(text="⭐⭐⭐⭐ 4+ stele", callback_data="filter|rep=4|p=1")],
            [InlineKeyboardButton(text="⭐⭐⭐⭐⭐ 5 stele", callback_data="filter|rep=5|p=1")],
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="sellers|type=filters")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
        text = "⭐ Filtrează după reputație:"
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("filter|sector="))
@router.callback_query(F.data.startswith("filter|prod="))
@router.callback_query(F.data.startswith("filter|rep="))
async def filter_results_callback(callback: CallbackQuery):
    data_parts = callback.data.split("|")
    filter_param = data_parts[1]
    page = int(data_parts[2].split("=")[1])
    
    marketplace_service = MarketplaceService()
    
    # Parse filter parameters
    sector = None
    product_id = None
    min_reputation = None
    
    if filter_param.startswith("sector="):
        sector = int(filter_param.split("=")[1])
        filter_text = f"Sector {sector}"
    elif filter_param.startswith("prod="):
        product_id = int(filter_param.split("=")[1])
        product = await marketplace_service.get_product_by_id(product_id)
        filter_text = f"Produs: {product.name}"
    elif filter_param.startswith("rep="):
        min_reputation = int(filter_param.split("=")[1])
        filter_text = f"Reputație: {min_reputation}+ stele"
    
    sellers = await marketplace_service.search_sellers(sector, product_id, min_reputation, page)
    
    if not sellers:
        text = f"🔍 Filtru: {filter_text}\n\nNu au fost găsiți selleri."
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Înapoi", callback_data="sellers|type=filters")],
            [InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")]
        ])
    else:
        text = f"🔍 Filtru: {filter_text}\n\nSelleri găsiți:\n\n"
        
        keyboard_buttons = []
        for seller in sellers:
            # Create seller info text
            location_text = f" - {seller.location.name}" if seller.location else ""
            seller_text = f"👤 {seller.display_name or seller.user.first_name}{location_text} ⭐{seller.reputation}"
            
            # Create chat link
            if seller.user.username:
                chat_url = f"https://t.me/{seller.user.username}"
            else:
                chat_url = f"tg://user?id={seller.user.tg_id}"
            
            keyboard_buttons.append([
                InlineKeyboardButton(text=seller_text, callback_data=f"seller|id={seller.id}"),
                InlineKeyboardButton(text="💬 Chat", url=chat_url)
            ])
        
        # Navigation buttons
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"filter|{filter_param}|p={page-1}"))
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Înapoi", callback_data="sellers|type=filters"))
        nav_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"filter|{filter_param}|p={page+1}"))
        
        keyboard_buttons.append(nav_buttons)
        keyboard_buttons.append([InlineKeyboardButton(text="🏠 Meniu principal", callback_data="nav|to=main")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

