import pytest
from app.core.user import create_user, get_user_by_tg_id, update_nickname, delete_user


@pytest.mark.asyncio
async def test_create_and_get_user(session):
    tg_id = 1234569
    nickname = "Test User"

    created = await create_user(tg_id, nickname)
    assert created is True

    user = await get_user_by_tg_id(tg_id)
    assert user is not None
    assert user.tg_nickname == nickname

    new_nickname = "Updated User"

    updated = await update_nickname(tg_id, new_nickname)
    assert updated is True

    user = await get_user_by_tg_id(tg_id)
    assert user.tg_nickname == new_nickname

    deleted = await delete_user(tg_id)
    assert deleted is True




