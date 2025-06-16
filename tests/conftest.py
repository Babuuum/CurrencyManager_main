import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db.db_core import Base

TEST_DB_URL = "postgresql+asyncpg://user:password@localhost:5434/db_test"

@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(TEST_DB_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(async_engine):
    Session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    async with Session() as session:
        yield session
        await session.rollback()