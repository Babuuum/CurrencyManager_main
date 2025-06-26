import os
import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy import select, delete

from app.app_factory import create_app
from app.db.db_core import SessionLocal
from app.db.models import Users, Asset

from aiogram.types import Message
from app.bot.bot import bot


from aiogram.client.session.base import BaseSession
from aiogram.methods import TelegramMethod
from typing import Any


load_dotenv()
app=create_app()


@pytest.mark.asyncio
async def test_fsm_create_asset(monkeypatch):
    class FakeSession(BaseSession):
        async def __call__(self, bot, method: TelegramMethod, timeout: float | None = None) -> Any:
            print(f"[MOCKED __call__]: {method}")
            return None

        async def make_request(self, bot, method: TelegramMethod) -> Any:
            print(f"[MOCKED make_request]: {method}")
            return None

        async def stream_content(self, *args, **kwargs) -> Any:
            print("[MOCKED stream_content]")
            return None

        async def close(self) -> None:
            print("[MOCKED close()]")



    monkeypatch.setattr(bot, "session", FakeSession())

    test_user_id = 222222
    test_username = "FSM Tester"
    test_asset_name = "BTC"
    test_asset_amount = 0.25

    async def fake_answer(self: Message, text: str, **kwargs):
        print(f"[MOCK]: {text}")
        return None

    monkeypatch.setattr(Message, "answer", fake_answer)

    transport = ASGITransport(app=app)
    tg_token = os.getenv("TG_BOT_TOKEN")
    base_url = "http://test"

    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        await ac.post(f"/webhook/{tg_token}", json={
            "update_id": 1,
            "message": {
                "message_id": 1,
                "from": {
                    "id": test_user_id,
                    "is_bot": False,
                    "first_name": "FSM",
                    "last_name": "Tester"
                },
                "chat": {
                    "id": test_user_id,
                    "first_name": "FSM",
                    "username": "fsm_test",
                    "type": "private"
                },
                "date": 1700000000,
                "text": "/start"
            }
        })

        await ac.post(f"/webhook/{tg_token}", json={
            "update_id": 2,
            "callback_query": {
                "id": "1",
                "from": {
                    "id": test_user_id,
                    "first_name": "FSM",
                    "username": "fsm_test",
                    "is_bot": False
                },
                "message": {
                    "message_id": 2,
                    "chat": {
                        "id": test_user_id,
                        "type": "private"
                    }
                },
                "chat_instance": "mock_instance_123",
                "data": "active:create"
            }
        })

        await ac.post(f"/webhook/{tg_token}", json={
            "update_id": 3,
            "message": {
                "message_id": 3,
                "from": {
                    "id": test_user_id,
                    "first_name": "FSM",
                    "is_bot": False

                },
                "chat": {
                    "id": test_user_id,
                    "type": "private"
                },
                "date": 1700000000,
                "text": test_asset_name
            }
        })

        await ac.post(f"/webhook/{tg_token}", json={
            "update_id": 4,
            "message": {
                "message_id": 4,
                "from": {
                    "id": test_user_id,
                    "first_name": "FSM",
                    "is_bot": False
                },
                "chat": {
                    "id": test_user_id,
                    "type": "private"
                },
                "date": 1700000000,
                "text": str(test_asset_amount)
            }
        })

    async with SessionLocal() as session:
        result = await session.execute(
            select(Users).where(Users.tg_id == test_user_id)
        )
        user = result.scalar_one_or_none()
        assert user is not None
        assert user.tg_nickname.startswith("FSM")

        result_asset = await session.execute(
            select(Asset).where(Asset.user_id == user.id, Asset.name == test_asset_name)
        )
        asset = result_asset.scalar_one_or_none()
        assert asset is not None
        assert asset.amount == test_asset_amount

        await session.delete(asset)
        await session.delete(user)
        await session.commit()
