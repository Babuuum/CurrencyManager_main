from sqlalchemy.future import select

from app.analytics.portfolio import get_total_value
from app.db.db_core import SessionLocal
from app.db.models import Users, Asset
from app.analytics.price_change import get_price_change

from app.services.coingecko import get_price
from app.analytics.history import save_asset_price
from app.utils.logger import logger


async def message_builder(user_tg_id: int, history: bool=False ) -> str:
        async with SessionLocal() as session:
            result = await session.execute(select(Users).where(Users.tg_id == user_tg_id))
            user = result.scalar_one_or_none()

            if not user:
                return "Пользователь не найден"

            assets_result = await session.execute(
                select(Asset).where(Asset.user_id == user.id)
            )
            assets = assets_result.scalars().all()

            if not assets:
                return "У вас нет подходящих активов"

            amount = await get_total_value(user_tg_id)

            message_lines = [f"💼 *Ваши активы:*\n"
                             f"💰 *Суммарная стоимость портфеля: {amount:,.2f}*"
                             ]
            for asset in assets:
                try:
                    price = await get_price(asset.name)
                    week_price_change = await get_price_change(asset.id, 7, price)
                    month_price_change = await get_price_change(asset.id, 30, price)

                    message_lines.append(
                        f"- {asset.name}: {asset.amount} ({asset.type}) \n"
                        f"  Цена: ${price}\n"
                        f"    за 7 дней: {week_price_change}\n"
                        f"    за 30 дней: {month_price_change}\n"
                    )

                    if history:
                        await save_asset_price(asset.id, price)

                except Exception as e:
                    logger.error(f"Ошибка обработки актива {asset.name}: {e}")

                message = "\n".join(message_lines)

            return message