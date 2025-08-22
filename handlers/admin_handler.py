from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.navigation import back_to_main_keyboard
from services.admin_service import AdminService
from config import OWNER_ID

router = Router()

def is_admin(user_id: int) -> bool:
    # In a real implementation, this would check against a list of admin IDs
    return user_id == OWNER_ID

@router.message(Command("add_seller"))
async def add_seller_command(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Nu ai permisiuni de admin.", reply_markup=back_to_main_keyboard())
        return
    
    # Parse command: /add_seller @username
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Folosește: /add_seller @username", reply_markup=back_to_main_keyboard())
        return
    
    username = parts[1].replace("@", "")
    admin_service = AdminService()
    
    success = await admin_service.add_seller(username)
    if success:
        await message.answer(f"✅ @{username} a fost adăugat ca seller.", reply_markup=back_to_main_keyboard())
    else:
        await message.answer(f"❌ Nu s-a putut adăuga @{username} ca seller.", reply_markup=back_to_main_keyboard())

@router.message(Command("remove_seller"))
async def remove_seller_command(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Nu ai permisiuni de admin.", reply_markup=back_to_main_keyboard())
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Folosește: /remove_seller @username", reply_markup=back_to_main_keyboard())
        return
    
    username = parts[1].replace("@", "")
    admin_service = AdminService()
    
    success = await admin_service.remove_seller(username)
    if success:
        await message.answer(f"✅ @{username} a fost eliminat din selleri.", reply_markup=back_to_main_keyboard())
    else:
        await message.answer(f"❌ Nu s-a putut elimina @{username} din selleri.", reply_markup=back_to_main_keyboard())

@router.message(Command("set_location"))
async def set_location_command(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Nu ai permisiuni de admin.", reply_markup=back_to_main_keyboard())
        return
    
    # Parse command: /set_location @username sector_number
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Folosește: /set_location @username <sector_number>", reply_markup=back_to_main_keyboard())
        return
    
    username = parts[1].replace("@", "")
    try:
        sector = int(parts[2])
    except ValueError:
        await message.answer("Sectorul trebuie să fie un număr (1-6).", reply_markup=back_to_main_keyboard())
        return
    
    admin_service = AdminService()
    success = await admin_service.set_seller_location(username, sector)
    
    if success:
        await message.answer(f"✅ @{username} a fost setat în Sectorul {sector}.", reply_markup=back_to_main_keyboard())
    else:
        await message.answer(f"❌ Nu s-a putut seta locația pentru @{username}.", reply_markup=back_to_main_keyboard())

@router.message(Command("set_product"))
async def set_product_command(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Nu ai permisiuni de admin.", reply_markup=back_to_main_keyboard())
        return
    
    # Parse command: /set_product @username prod1,prod2,prod3
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Folosește: /set_product @username <prod1,prod2,...>", reply_markup=back_to_main_keyboard())
        return
    
    username = parts[1].replace("@", "")
    products = [p.strip() for p in parts[2].split(",")]
    
    admin_service = AdminService()
    success = await admin_service.set_seller_products(username, products)
    
    if success:
        await message.answer(f"✅ Produsele au fost setate pentru @{username}: {', '.join(products)}", reply_markup=back_to_main_keyboard())
    else:
        await message.answer(f"❌ Nu s-au putut seta produsele pentru @{username}.", reply_markup=back_to_main_keyboard())

@router.message(Command("add_product"))
async def add_product_command(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Nu ai permisiuni de admin.", reply_markup=back_to_main_keyboard())
        return
    
    # Parse command: /add_product <name> [description]
    parts = message.text.split(maxsplit=2)
    if len(parts) < 2:
        await message.answer("Folosește: /add_product <nume> [descriere]", reply_markup=back_to_main_keyboard())
        return
    
    name = parts[1]
    description = parts[2] if len(parts) > 2 else None
    
    admin_service = AdminService()
    success = await admin_service.add_product(name, description)
    
    if success:
        await message.answer(f"✅ Produsul '{name}' a fost adăugat.", reply_markup=back_to_main_keyboard())
    else:
        await message.answer(f"❌ Nu s-a putut adăuga produsul '{name}'.", reply_markup=back_to_main_keyboard())

@router.message(Command("give_rank"))
async def give_rank_command(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Nu ai permisiuni de admin.", reply_markup=back_to_main_keyboard())
        return
    
    # Parse command: /give_rank @username level
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Folosește: /give_rank @username <nivel>", reply_markup=back_to_main_keyboard())
        return
    
    username = parts[1].replace("@", "")
    try:
        level = int(parts[2])
    except ValueError:
        await message.answer("Nivelul trebuie să fie un număr (0-5).", reply_markup=back_to_main_keyboard())
        return
    
    admin_service = AdminService()
    success = await admin_service.give_rank(username, level)
    
    if success:
        await message.answer(f"✅ @{username} a primit rank-ul nivel {level}.", reply_markup=back_to_main_keyboard())
    else:
        await message.answer(f"❌ Nu s-a putut acorda rank-ul pentru @{username}.", reply_markup=back_to_main_keyboard())

@router.message(Command("give_grad"))
async def give_grad_command(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Nu ai permisiuni de admin.", reply_markup=back_to_main_keyboard())
        return
    
    # Parse command: /give_grad @username grad
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Folosește: /give_grad @username <grad>", reply_markup=back_to_main_keyboard())
        return
    
    username = parts[1].replace("@", "")
    grade = parts[2]
    
    admin_service = AdminService()
    success = await admin_service.give_grade(username, grade)
    
    if success:
        await message.answer(f"✅ @{username} a primit gradul '{grade}'.", reply_markup=back_to_main_keyboard())
    else:
        await message.answer(f"❌ Nu s-a putut acorda gradul pentru @{username}.", reply_markup=back_to_main_keyboard())

@router.message(Command("confirm_order"))
async def confirm_order_command(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Nu ai permisiuni de admin.", reply_markup=back_to_main_keyboard())
        return
    
    # Parse command: /confirm_order txn_id
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Folosește: /confirm_order <txn_id>", reply_markup=back_to_main_keyboard())
        return
    
    try:
        txn_id = int(parts[1])
    except ValueError:
        await message.answer("ID-ul tranzacției trebuie să fie un număr.", reply_markup=back_to_main_keyboard())
        return
    
    admin_service = AdminService()
    success = await admin_service.confirm_order(txn_id)
    
    if success:
        await message.answer(f"✅ Tranzacția #{txn_id} a fost confirmată. Buyer-ul a primit +25 XP.", reply_markup=back_to_main_keyboard())
    else:
        await message.answer(f"❌ Nu s-a putut confirma tranzacția #{txn_id}.", reply_markup=back_to_main_keyboard())

