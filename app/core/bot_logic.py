from datetime import datetime

from sqlalchemy import select, update, delete
from app.db.db_core import SessionLocal
from app.db.models import Users, Asset
from app.utils.logger import logger


async def get_user_by_tg_id(tg_id: int):
    async with SessionLocal() as session:
        stmt = select(Users).where(Users.tg_id == tg_id)
        result = await session.scalar(stmt)
        return result


async def create_asset(tg_id: int, name: str, amount: float, type_: str = "manual") -> bool:
    async with SessionLocal() as session:
        user = await get_user_by_tg_id(tg_id)
        if not user:
            logger.warning(f"User not found: {tg_id}")
            return False

        asset = Asset(
            user_id=user.id,
            name=name.upper(),
            amount=amount,
            type=type_,
            created_at=datetime.utcnow()
        )

        session.add(asset)
        try:
            await session.commit()
            logger.info(f"Asset created: {name} ({amount}) for user {tg_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to create asset: {e}")
            return False


async def update_asset_amount(tg_id: int, name: str, amount: float) -> bool:
    async with SessionLocal() as session:
        user = await get_user_by_tg_id(tg_id)
        if not user:
            return False

        stmt = select(Asset).where(Asset.user_id == user.id, Asset.name == name.upper())
        asset = await session.scalar(stmt)

        if not asset:
            return False

        asset.amount = amount
        try:
            await session.commit()
            logger.info(f"Asset updated: {name} → {amount} (user: {tg_id})")
            return True
        except Exception as e:
            logger.error(f"Failed to update asset: {e}")
            return False


async def delete_asset(tg_id: int, name: str) -> bool:
    async with SessionLocal() as session:
        user = await get_user_by_tg_id(tg_id)
        if not user:
            return False

        stmt = select(Asset).where(Asset.user_id == user.id, Asset.name == name.upper())
        asset = await session.scalar(stmt)

        if not asset:
            return False

        await session.delete(asset)
        try:
            await session.commit()
            logger.info(f"Asset deleted: {name} (user: {tg_id})")
            return True
        except Exception as e:
            logger.error(f"Failed to delete asset: {e}")
            return False
