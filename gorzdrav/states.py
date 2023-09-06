from aiogram.fsm.state import StatesGroup, State


class AppointmentStates(StatesGroup):
    district = State()
    clinic = State()
    speciality = State()
    doctor = State()
    appointment = State()