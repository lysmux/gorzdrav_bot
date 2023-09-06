from aiogram.fsm.state import StatesGroup, State


class ProfileStates(StatesGroup):
    last_name = State()
    first_name = State()
    middle_name = State()
    birthdate = State()


class ProfileActionStates(StatesGroup):
    select = State()
    delete_confirm = State()
