from aiogram.fsm.state import StatesGroup, State


class TrackingStates(StatesGroup):
    list = State()
    action = State()
    status = State()
    deleted = State()
