from sqlalchemy import select
from app.db.db_core import SessionLocal
from app.db.models import Users
from app.utils.logger import logger


async def get_user_by_tg_id(tg_id: int):
    async with SessionLocal() as session:
        stmt = select(Users).where(Users.tg_id == tg_id)
        return await session.scalar(stmt)


async def create_user(tg_id: int, nickname: str) -> bool:
    async with SessionLocal() as session:
        exists = await get_user_by_tg_id(tg_id)
        if exists:
            logger.info(f"Пользователь {tg_id} уже существует")
            return False

        new_user = Users(tg_id=tg_id, tg_nickname=nickname)
        session.add(new_user)

        try:
            await session.commit()
            logger.info(f"Создан новый пользователь: {nickname} ({tg_id})")
            return True
        except Exception as e:
            logger.error(f"Ошибка создания пользователя: {e}")
            return False


async def update_nickname(tg_id: int, new_nickname: str) -> bool:
    async with SessionLocal() as session:
        stmt = select(Users).where(Users.tg_id == tg_id)
        user = await session.scalar(stmt)

        if not user:
            logger.warning(f"Пользователь не найден: {tg_id}")
            return False

        user.tg_nickname = new_nickname

        try:
            await session.commit()
            logger.info(f"Обновлен ник пользователя: {tg_id} → {new_nickname}")
            return True
        except Exception as e:
            logger.error(f"Ошибка обновления ника: {e}")
            return False

async def delete_user(tg_id: int) -> bool:
    async with SessionLocal() as session:
        stmt = select(Users).where(Users.tg_id == tg_id)
        user = await session.scalar(stmt)

        if not user:
            logger.warning(f"Пользователь не найден: {tg_id}")
            return False

        await session.delete(user)

        try:
            await session.commit()
            logger.info(f"Пользователь удален: {tg_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления пользователя: {e}")
            return False