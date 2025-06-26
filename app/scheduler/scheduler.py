from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from sqlalchemy.future import select

from app.core.message import message_builder
from app.db.db_core import SessionLocal
from app.db.models import Users
from app.utils.logger import logger
from pytz import timezone

scheduler = AsyncIOScheduler()


async def send_daily_summary(bot: Bot):
    async with SessionLocal() as session:
        result = await session.execute(select(Users))
        users = result.scalars().all()

        for user in users:
            new_message = await message_builder(user_tg_id=user.tg_id, history=True)

            try:
                await bot.send_message(
                    chat_id=user.tg_id,
                    text=new_message,
                    parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"❌ Ошибка отправки пользователю {user.tg_id}: {e}")


def setup_scheduler(bot: Bot):
    scheduler.add_job(
        send_daily_summary,
        trigger=CronTrigger(hour=10, minute=0, timezone=timezone("Europe/Moscow")),
        args=[bot],
        id="daily_summary_job",
        replace_existing=True,
    )
    scheduler.start()