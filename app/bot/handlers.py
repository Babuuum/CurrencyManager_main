from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.bot.keyboards import actives_menu, main_menu
from app.bot.states import ActiveCreateState, ActiveUpdateState, ActiveDeleteState
from app.services.coingecko import get_price
from app.utils.logger import logger
from app.core.message import message_builder
from app.core.bot_logic import create_asset, delete_asset
from app.core.user import create_user, get_user_by_tg_id


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()

    exists = await get_user_by_tg_id(user_id)

    if exists:
        logger.info(f"User {user_id} уже зарегистрирован")
        await message.answer("Welcome back!", reply_markup=main_menu())
    else:
        await create_user(user_id, user_name)
        await message.answer("Вы успешно зарегистрированы!", reply_markup=main_menu())


@router.message(F.text == "📊 Actives")
async def cmd_actives(message: Message):
    new_message = await message_builder(user_tg_id=message.from_user.id, history=False)
    await message.answer(
        text=new_message,
        reply_markup=actives_menu()
    )

@router.callback_query(F.data == "active:create")
async def handle_active_create(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название актива (пример: BTC, ETH):")
    await state.set_state(ActiveCreateState.waiting_for_active_name)
    await callback.answer()

@router.message(ActiveCreateState.waiting_for_active_name)
async def input_active_name(message: Message, state: FSMContext):
    try:
        await get_price(message.text)
    except:
        await message.answer("Имя актива введенно в неверном формате")
        return

    await state.update_data(name=message.text)
    await message.answer("Введите количество актива:")
    await state.set_state(ActiveCreateState.waiting_for_active_amount)

@router.message(ActiveCreateState.waiting_for_active_amount)
async def input_active_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    success = await create_asset(message.from_user.id, data["name"], float(message.text))

    if success:
        await message.answer("✅ Актив добавлен", reply_markup=main_menu())
    else:
        await message.answer("❌ Ошибка добавления актива")

@router.callback_query(F.data.startswith("active:update"))
async def handle_active_update(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название актива (пример: BTC, ETH):")
    await state.set_state(ActiveUpdateState.waiting_for_active_name)
    await callback.answer()

@router.message(ActiveUpdateState.waiting_for_active_name)
async def input_active_name_update(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите количество актива:")
    await state.set_state(ActiveUpdateState.waiting_for_active_amount)

@router.message(ActiveUpdateState.waiting_for_active_amount)
async def input_active_amount_update(message: Message, state: FSMContext):
    data = await state.get_data()
    success = await create_asset(message.from_user.id, data["name"], float(message.text))

    if success:
        await message.answer("✅ Актив Обновлен", reply_markup=main_menu())
    else:
        await message.answer("❌ Ошибка Обновления актива")

@router.callback_query(F.data.startswith("active:delete"))
async def handle_active_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название актива (пример: BTC, ETH):")
    await state.set_state(ActiveDeleteState.waiting_for_active_name)
    await callback.answer()

@router.message(ActiveDeleteState.waiting_for_active_name)
async def input_active_name_delete(message: Message):
    success = delete_asset(message.from_user.id, message.text)

    if success:
        await message.answer("✅ Актив Удален", reply_markup=main_menu())
    else:
        await message.answer("❌ Ошибка Удаления актива")

@router.callback_query(F.data.startswith("active:quit"))
async def handle_active_quit(callback: CallbackQuery):
    await callback.message.answer("chose option",reply_markup = main_menu())

@router.message(F.text == "💰 incomes")
async def cmd_incomes(message: Message):
    await message.answer('this function in development!')

@router.message(F.text == "⚙️ Settings")
async def cmd_settings(message: Message):
    await message.answer('this function in development!')