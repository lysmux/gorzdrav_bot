from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    action = State()
    statistics = State()
