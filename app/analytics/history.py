from datetime import datetime, timezone
from app.db.db_core import SessionLocal
from app.db.models import Data
from app.utils.logger import logger


async def save_asset_price(asset_id: int, price: float) -> None:
    async with SessionLocal() as session:
        new_data = Data(
            asset_id=asset_id,
            datetime=datetime.now(timezone.utc),
            exchange_rate=price
        )
        session.add(new_data)
        await session.commit()

        logger.info(f"Цена актива добавлена в базу: {asset_id}:{price}")