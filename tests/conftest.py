import os
import asyncio
import platform

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.db import db_core
from app.db.models import Base, Users

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

DATABASE_URL = os.getenv("TEST_DB_URL")

engine_test = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncTestSession = async_sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def session() -> AsyncSession:
    async with AsyncTestSession() as session:
        yield session


@pytest.fixture(autouse=True)
def override_session(monkeypatch):
    monkeypatch.setattr(db_core, "SessionLocal", AsyncTestSession)
    monkeypatch.setattr(db_core, "engine", engine_test)

@pytest.fixture(scope="module")
async def test_db():
    async with AsyncSession() as session:
        user = Users(tg_id=123456, tg_nickname="Test")
        session.add(user)
        await session.commit()
        yield session
