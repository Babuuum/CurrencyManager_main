import os

from dotenv import load_dotenv

from sqlalchemy import MetaData, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DB_URL = os.getenv('DB_URL')
import os

if os.getenv("IS_TEST") == "true":
    DATABASE_URL = os.getenv("DB_URL")
else:
    DATABASE_URL = os.getenv("TEST_DB_URL")

engine = create_async_engine(
    DB_URL,
    echo=True,
    future=True,
    poolclass=NullPool
)

metadata = MetaData()


class Base(DeclarativeBase):
    pass


SessionLocal = async_sessionmaker(bind=engine)

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
