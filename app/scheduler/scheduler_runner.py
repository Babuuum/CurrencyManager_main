import asyncio
from aiogram import Bot
from dotenv import load_dotenv
import os

from app.scheduler.scheduler import setup_scheduler
from app.utils.logger import logger

load_dotenv()

async def main():
    bot = Bot(token=os.getenv("tg_bot_token"))
    setup_scheduler(bot)

    logger.info("📅 Планировщик запущен")
    while True:
        await asyncio.sleep(60 * 60)  # держим процесс живым

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Остановлено вручную")