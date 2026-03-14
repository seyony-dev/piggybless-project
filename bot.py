import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db import init_db
from handlers import router
from scheduler import setup_scheduler, schedule_daily_blessings

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    scheduler = setup_scheduler(bot)
    scheduler.start()
    
    # We will trigger the planning logic on startup to schedule messages for the current day
    # if the bot was restarted after 00:00.
    await schedule_daily_blessings(bot, scheduler)
    
    try:
        print("Bot is starting...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
