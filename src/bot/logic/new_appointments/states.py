from aiogram.fsm.state import StatesGroup, State


class NewAppointmentsStates(StatesGroup):
    notify = State()
