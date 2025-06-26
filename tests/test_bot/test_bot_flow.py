import os

import pytest

from dotenv import load_dotenv
from select import select

from app.app_factory import create_app
from app.db.db_core import SessionLocal
from app.db.models import Users
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy import select


load_dotenv()

app=create_app()


@pytest.mark.asyncio
async def test_start_and_add_asset(monkeypatch):
    from aiogram.types import Message
    from app.bot.bot import bot

    async def fake_answer(self: Message, text: str, **kwargs):
        assert "Welcome" in text or "зарегистрированы" in text
        return None

    monkeypatch.setattr(Message, "answer", fake_answer)

    start_payload = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 111111,
                "is_bot": False,
                "first_name": "Tester",
                "username": "testuser",
                "language_code": "en"
            },
            "chat": {
                "id": 111111,
                "first_name": "Tester",
                "username": "testuser",
                "type": "private"
            },
            "date": 1700000000,
            "text": "/start"
        }
    }

    transport = ASGITransport(app=app)
    tg_token = os.getenv("TG_BOT_TOKEN")

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(f"/webhook/{tg_token}", json=start_payload)

    assert response.status_code == 200
    assert response.json()["ok"] is True

    async with SessionLocal() as session:
        stmt = select(Users).where(Users.tg_id == 111111)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        assert user is not None

        await session.delete(user)
        await session.commit()


        deleted = await session.scalar(select(Users).where(Users.tg_id == 111111))
        assert deleted is None

