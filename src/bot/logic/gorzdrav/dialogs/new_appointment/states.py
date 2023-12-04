from aiogram.fsm.state import StatesGroup, State


class NewAppointmentStates(StatesGroup):
    notify = State()
