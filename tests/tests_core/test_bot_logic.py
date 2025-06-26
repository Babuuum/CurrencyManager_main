import pytest
from app.core.bot_logic import create_asset, update_asset_amount, delete_asset
from app.core.user import create_user

@pytest.mark.asyncio
async def test_create_update_delete_asset(session):
    tg_id = 555555
    await create_user(tg_id, "Tester")

    created = await create_asset(tg_id, "ETH", 2.0)
    assert created

    updated = await update_asset_amount(tg_id, "ETH", 3.0)
    assert updated

    deleted = await delete_asset(tg_id, "ETH")
    assert deleted
