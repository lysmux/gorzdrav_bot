from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from bot.gorzdrav.states import AppointmentStates
from bot.utils.template_engine import render_template
from gorzdrav_api.utils import generate_gorzdrav_url

router = Router()


@router.message(AppointmentStates.appointment)
async def appointment_handler(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    district = state_data["selected_district"]
    clinic = state_data["selected_clinic"]
    speciality = state_data["selected_speciality"]
    doctor = state_data["selected_doctor"]

    appointments = state_data["appointments"]
    selected_appointment = next(filter(lambda x: x.time_str == message.text, appointments), None)

    if selected_appointment:
        url = generate_gorzdrav_url(
            district=district.id,
            clinic=clinic.id,
            speciality=speciality.id,
            doctor=doctor.id,
        )

        await message.answer(text=render_template("success/make_appointment.html", url=url))
    else:
        await message.answer(text=render_template("errors/unknown_appointment.html", appointment=message.text))
