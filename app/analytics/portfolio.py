from sqlalchemy.future import select

from app.db.db_core import SessionLocal
from app.db.models import Users
from app.services.coingecko import get_price
from app.utils.logger import logger


async def get_total_value(user_id: int) -> float:
    async with SessionLocal() as session:
        stmt =  select(Users).where(tg_id=user_id)
        user = await session.scalar(stmt)

        result = 0

        for asset in user.assets:
            price = await get_price(asset.name)
            result += price * asset.amount

        logger.info(f'Посчитаны все активы пользователя: {user.tg_nickname}')

        return result