import os

from dotenv import load_dotenv

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

engine = create_async_engine( f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}", echo=True)

metadata = MetaData()


class Base(DeclarativeBase):
    pass


SessionLocal = async_sessionmaker(bind=engine)

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
