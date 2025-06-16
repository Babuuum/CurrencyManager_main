from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from aiogram import Bot
from sqlalchemy.future import select

from app.analytics.portfolio import get_total_value
from app.db.db_core import SessionLocal
from app.db.models import Users, Asset
from app.analytics.price_change import get_price_change

from app.services.coingecko import get_price
from app.analytics.history import save_asset_price
from app.utils.logger import logger

scheduler = AsyncIOScheduler()


async def send_daily_summary(bot: Bot):
    async with SessionLocal() as session:
        result = await session.execute(select(Users))
        users = result.scalars().all()

        for user in users:
            assets_result = await session.execute(
                select(Asset).where(Asset.user_id == user.id)
            )
            assets = assets_result.scalars().all()

            if not assets:
                continue

            amount = await get_total_value(user.tg_id)

            message_lines = [f"💼 *Ваши активы:*\n"
                             f"💰 *Суммарная стоимость портфеля: {amount:,.2f}*"
                             ]
            for asset in assets:
                price = await get_price(asset.name)

                week_price_change = await get_price_change(asset.id, 7, price)
                month_price_change = await get_price_change(asset.id, 30, price)



                message_lines.append(f"- {asset.name}: {asset.amount} ({asset.type}) \n"
                                     f"  Цена: ${price}\n "
                                     f"    за 7 дней: {week_price_change}\n"
                                     f"    за 30 дней: {month_price_change}\n"
                                     )

                try:
                    await save_asset_price(asset.id, price)
                except Exception as e:
                    logger.error(f"❌ Ошибка сохранения курса {asset.name} в базу данных: {e}")

            message = "\n".join(message_lines)

            try:
                await bot.send_message(
                    chat_id=user.tg_id,
                    text=message,
                    parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"❌ Ошибка отправки пользователю {user.tg_id}: {e}")


def setup_scheduler(bot: Bot):
    scheduler.add_job(
        send_daily_summary,
        trigger=IntervalTrigger(minutes=1),  # для теста; позже заменим на cron
        args=[bot],
        id="daily_summary_job",
        replace_existing=True,
    )
    scheduler.start()