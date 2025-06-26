from aiogram.fsm.state import StatesGroup, State


class ActiveCreateState(StatesGroup):
    waiting_for_active_name = State()
    waiting_for_active_amount = State()

class ActiveUpdateState(StatesGroup):
    waiting_for_active_name = State()
    waiting_for_active_amount = State()

class ActiveDeleteState(StatesGroup):
    waiting_for_active_name = State()