import pytest
from sqlalchemy import delete
from unittest.mock import AsyncMock

from app.db.models import Users
from app.scheduler.scheduler import send_daily_summary
from tests.conftest import session


@pytest.mark.asyncio
async def test_send_daily_summary(session, monkeypatch):
    test_user_id = 123456789

    monkeypatch.setattr("app.scheduler.scheduler.SessionLocal", lambda: session)

    await session.execute(delete(Users))
    await session.commit()

    test_user = Users(tg_id=test_user_id, tg_nickname="MockUser")
    session.add(test_user)
    await session.commit()

    fake_bot = AsyncMock()
    monkeypatch.setattr("app.scheduler.scheduler.message_builder", AsyncMock(return_value="Test Summary"))

    await send_daily_summary(fake_bot)

    fake_bot.send_message.assert_awaited_once_with(
        chat_id=test_user_id,
        text="Test Summary",
        parse_mode="Markdown"
    )

    await session.execute(delete(Users).where(Users.tg_id == test_user_id))
    await session.commit()
