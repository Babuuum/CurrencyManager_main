from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from sqlalchemy.future import select

from app.db.db_core import SessionLocal
from app.db.models import Users
from app.utils.logger import logger

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_name = f"{message.from_user.first_name} {message.from_user.last_name}"

    async with SessionLocal() as session:
        result = await session.execute(select(Users).where(Users.tg_id == user_id))
        db_user = result.scalar_one_or_none()

        if db_user:
            logger.info(f'authentication {user_name} is complete')
            await message.answer("Welcome to the Currency Manager bot!")
            return True
        else:
            new_user = Users(tg_nickname=user_name, tg_id=user_id)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            logger.info(f'authorisation {user_name} is complete')
            return new_user


