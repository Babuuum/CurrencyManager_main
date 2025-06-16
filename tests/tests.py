import pytest
from app.schemas import UserCreate
from app.crud import create_user

@pytest.mark.asyncio
async def test_create_user(db_session):
    user_data = UserCreate(username="alice", email="alice@example.com")
    user = await create_user(db_session, user_data)

    assert user.id is not None
    assert user.username == "alice"
    assert user.email == "alice@example.com"