from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.db_core import SessionLocal
from app.db.models import Users
from app.services.coingecko import get_price
from app.utils.logger import logger


async def get_total_value(user_id: int) -> float:
    async with SessionLocal() as session:
        result = await session.execute(
            select(Users)
            .options(selectinload(Users.assets))
            .where(Users.tg_id == user_id)
        )
        user = result.scalar_one_or_none()

        result = 0

        for asset in user.assets:
            price = await get_price(asset.name)
            result += price * asset.amount

        logger.info(f'Посчитаны все активы пользователя: {user.tg_nickname}')

        return result