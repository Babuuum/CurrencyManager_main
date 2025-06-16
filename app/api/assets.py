from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_core import get_session
from app.db.models import Asset
from app.schemas.asset import AssetRead, AssetCreate, AssetUpdate

from sqlalchemy.future import select

from app.utils.logger import logger

router = APIRouter()

@router.get('/', response_model=list[AssetRead])
async def get_assets(session: AsyncSession = Depends(get_session)):
    user_id = 1 #vremenno
    result = await session.execute(select(Asset).where(Asset.user_id == user_id))
    logger.info(f"User assets was send: {user_id}")
    return result.all()

@router.post('/', response_model=list[AssetRead])
async def create_asset(asset: AssetCreate ,session: AsyncSession = Depends(get_session)):
    user_id = 1
    new_asset = Asset(**asset.dict(), user_id=user_id)
    session.add(new_asset)
    await session.commit()
    await session.refresh(new_asset)
    logger.info(f"Asset was created: {user_id}:{new_asset.name}")
    return new_asset

@router.put("/{asset_id}", response_model=AssetRead)
async def update_asset(asset_id: int, asset: AssetUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Asset).where(Asset.id == asset_id))
    existing = result.scalar_one_or_none()
    if not existing:
        logger.warning(f"Asset not found : {asset_id}")
        raise HTTPException(status_code=404, detail="Asset not found")
    for key, value in asset.dict(exclude_unset=True).items():
        setattr(existing, key, value)
    await session.commit()
    await session.refresh(existing)
    logger.info(f"Asset was refreshed: {asset_id}")
    return existing

@router.delete("/{asset_id}")
async def delete_asset(asset_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Asset).where(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        logger.warning(f"Asset not found : {asset_id}")
        raise HTTPException(status_code=404, detail="Asset not found")
    await session.delete(asset)
    await session.commit()

    logger.info(f"Asset was deleted: {asset_id}")

    return {"status": "deleted"}

