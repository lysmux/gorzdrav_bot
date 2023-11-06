from aiogram.fsm.state import StatesGroup, State


class AddTrackingStates(StatesGroup):
    add = State()
    added = State()
