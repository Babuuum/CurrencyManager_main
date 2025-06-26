from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.bot.handlers import router
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TG_BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(router)