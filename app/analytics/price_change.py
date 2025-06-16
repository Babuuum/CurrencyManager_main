from datetime import datetime
from datetime import timedelta

from app.db.db_core import SessionLocal
from app.db.models import Users, Asset, Data
from sqlalchemy.future import select

from app.utils.logger import logger


async def get_price_change(asset_id: int, delta_days: int, new_data: float) -> str:
    async with SessionLocal() as session:
        threshold = datetime.utcnow() - timedelta(days=delta_days)

        result = await session.execute(
            select(Data)
            .where(Data.asset_id == asset_id, Data.datetime <= threshold)
            .order_by(Data.datetime.desc())
            .limit(1)
        )
        old_data = result.scalar_one_or_none()

        if not old_data or not new_data:
            logger.warning(f'Недостаточно данных для формирования истории актива: {asset_id}')
            return "н/д"

        diff = ((new_data - old_data.exchange_rate) / old_data.exchange_rate) * 100

        logger.info(f'Изменение курса {asset_id} равно: {diff:+.2f}%')

        return f"{diff:+.2f}%"
