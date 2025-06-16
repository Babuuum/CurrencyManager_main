import asyncio

from app.db.db_core import Base, engine
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DateTime, func, Float
from sqlalchemy import ForeignKey
from typing import List


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    tg_nickname: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    assets: Mapped[List["Asset"]] = relationship(back_populates="user")

class Asset(Base):
    __tablename__ = "asset"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)  # currency name
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False) # manual or wallet
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["Users"] = relationship(back_populates="assets")
    data: Mapped[List["Data"]] = relationship(back_populates="asset")

class Data(Base):
    __tablename__ = "data"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id", ondelete="CASCADE"), nullable=False)
    datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    exchange_rate: Mapped[float] = mapped_column(Float, nullable=False)

    asset: Mapped["Asset"] = relationship(back_populates="data")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__=='__main__':
    asyncio.run(create_tables())