import pytest
from datetime import datetime
from sqlalchemy import select

from app.db.models import Users, Asset


@pytest.mark.asyncio
async def test_asset_model_on_test_db(session):
    user = Users(tg_id=999999, tg_nickname="TestUser")
    session.add(user)
    await session.commit()
    await session.refresh(user)

    asset = Asset(
        user_id=user.id,
        name="BTC",
        amount=0.5,
        type="manual",
        created_at=datetime.utcnow()
    )
    session.add(asset)
    await session.commit()
    await session.refresh(asset)

    result = await session.execute(select(Asset).where(Asset.user_id == user.id))
    asset_db = result.scalar_one()
    assert asset_db.name == "BTC"
    assert asset_db.amount == 0.5

    await session.delete(asset_db)
    await session.delete(user)
    await session.commit()

    res = await session.execute(select(Asset).where(Asset.user_id == user.id))
    assert res.scalar_one_or_none() is None

    res2 = await session.execute(select(Users).where(Users.id == user.id))
    assert res2.scalar_one_or_none() is None
