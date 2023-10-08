from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from bot.gorzdrav.keyboards.callbacks import AppointmentCallback
from bot.gorzdrav.states import AppointmentStates
from bot.utils.template_engine import render_template
from gorzdrav_api.utils import generate_gorzdrav_url

router = Router()


@router.callback_query(
    AppointmentStates.appointment,
    AppointmentCallback.filter()
)
async def appointment_handler(
        call: types.CallbackQuery,
        callback_data: AppointmentCallback,
        state: FSMContext
):
    state_data = await state.get_data()
    district = state_data["selected_district"]
    clinic = state_data["selected_clinic"]
    speciality = state_data["selected_speciality"]
    doctor = state_data["selected_doctor"]

    appointments = state_data["appointments"]
    selected_appointment = next(filter(lambda x: x.id == callback_data.id, appointments))  # for future

    url = generate_gorzdrav_url(
        district=district.id,
        clinic=clinic.id,
        speciality=speciality.id,
        doctor=doctor.id,
    )

    await call.message.edit_text(text=render_template("gorzdrav/appointment/go_url.html", url=url))
