import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from services.database import init_db
from utils.init_data import initialize_all_data

# Import all handlers
from handlers import (
    start_handler,
    help_handler,
    profile_handler,
    faq_handler,
    tutoriale_handler,
    market_handler,
    seller_handler,
    referral_handler,
    ranking_handler,
    clasament_handler,
    asistenta_handler,
    grup_handler,
    giveaway_handler,
    lottery_handler,
    admin_handler,
    navigation_handler
)

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Include all routers
    dp.include_router(start_handler.router)
    dp.include_router(help_handler.router)
    dp.include_router(profile_handler.router)
    dp.include_router(faq_handler.router)
    dp.include_router(tutoriale_handler.router)
    dp.include_router(market_handler.router)
    dp.include_router(seller_handler.router)
    dp.include_router(referral_handler.router)
    dp.include_router(ranking_handler.router)
    dp.include_router(clasament_handler.router)
    dp.include_router(asistenta_handler.router)
    dp.include_router(grup_handler.router)
    dp.include_router(giveaway_handler.router)
    dp.include_router(lottery_handler.router)
    dp.include_router(admin_handler.router)
    dp.include_router(navigation_handler.router)

    # Initialize database and data
    await init_db()
    await initialize_all_data()

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

