from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot import bot_asnwers
from bot.gorzdrav.keyboards.reply import generate_keyboard
from bot.gorzdrav.states import AppointmentStates
from bot.middlewares.gorzdrav_api import GorZdravAPIMiddleware
from gorzdrav_api.api import GorZdravAPI

router = Router()
router.message.middleware(GorZdravAPIMiddleware())
router.callback_query.middleware(GorZdravAPIMiddleware())


@router.message(Command("make_appointment"))
async def make_appointment_handler(message: types.Message, state: FSMContext, gorzdrav_api: GorZdravAPI):
    districts = await gorzdrav_api.get_districts()
    keyboard = generate_keyboard(districts)

    await state.set_state(AppointmentStates.district)
    await state.update_data(districts=districts)
    await message.answer(text=bot_asnwers.DISTRICT_SELECT, reply_markup=keyboard)


@router.message(AppointmentStates.district)
async def district_handler(message: types.Message, state: FSMContext, gorzdrav_api: GorZdravAPI):
    districts = (await state.get_data())["districts"]
    selected_district = next(filter(lambda x: x.name == message.text, districts), None)

    if selected_district:
        clinics = await gorzdrav_api.get_clinics(selected_district)
        keyboard = generate_keyboard(clinics)
        await state.set_state(AppointmentStates.clinic)
        await state.update_data(clinics=clinics, selected_district=selected_district)
        await message.answer(text=bot_asnwers.CLINIC_SELECT, reply_markup=keyboard)
    else:
        await message.answer(text=bot_asnwers.UNKNOWN_DISTRICT.format(district=message.text))


@router.message(AppointmentStates.clinic)
async def clinic_handler(message: types.Message, state: FSMContext, gorzdrav_api: GorZdravAPI):
    clinics = (await state.get_data())["clinics"]
    selected_clinic = next(filter(lambda x: x.name == message.text, clinics), None)

    if selected_clinic:
        specialities = await gorzdrav_api.get_specialities(selected_clinic)
        keyboard = generate_keyboard(specialities)
        await state.set_state(AppointmentStates.speciality)
        await state.update_data(specialities=specialities, selected_clinic=selected_clinic)
        await message.answer(text=bot_asnwers.SPECIALITY_SELECT, reply_markup=keyboard)
    else:
        await message.answer(text=bot_asnwers.UNKNOWN_CLINIC.format(clinic=message.text))


@router.message(AppointmentStates.speciality)
async def speciality_handler(message: types.Message, state: FSMContext, gorzdrav_api: GorZdravAPI):
    state_data = await state.get_data()
    specialities = state_data["specialities"]
    selected_clinic = state_data["selected_clinic"]
    selected_speciality = next(filter(lambda x: x.name == message.text, specialities), None)

    if selected_speciality:
        doctors = await gorzdrav_api.get_doctors(selected_clinic, selected_speciality)
        keyboard = generate_keyboard(doctors)
        await state.set_state(AppointmentStates.doctor)
        await state.update_data(doctors=doctors, selected_speciality=selected_speciality)
        await message.answer(text=bot_asnwers.DOCTOR_SELECT, reply_markup=keyboard)
    else:
        await message.answer(text=bot_asnwers.UNKNOWN_SPECIALITY.format(speciality=message.text))


@router.message(AppointmentStates.doctor)
async def doctor_handler(message: types.Message, state: FSMContext, gorzdrav_api: GorZdravAPI):
    state_data = await state.get_data()
    doctors = state_data["doctors"]
    selected_clinic = state_data["selected_clinic"]
    selected_doctor = next(filter(lambda x: x.name == message.text, doctors), None)

    if selected_doctor:
        appointments = await gorzdrav_api.get_appointments(selected_clinic, selected_doctor)
        if appointments:
            keyboard = generate_keyboard(appointments)
            await state.set_state(AppointmentStates.appointment)
            await state.update_data(appointments=appointments, selected_doctor=selected_doctor)
            await message.answer(text=bot_asnwers.APPOINTMENT_SELECT, reply_markup=keyboard)
        else:
            await message.answer(text=bot_asnwers.NO_APPOINTMENTS)
    else:
        await message.answer(text=bot_asnwers.UNKNOWN_DOCTOR.format(doctor=message.text))


@router.message(AppointmentStates.appointment)
async def appointment_handler(message: types.Message, state: FSMContext):
    doctors = (await state.get_data())["appointments"]
    selected_appointment = next(filter(lambda x: x.name == message.text, doctors), None)

    if selected_appointment:
        await message.answer(text="Скоро будет запись")
    else:
        await message.answer(text=bot_asnwers.UNKNOWN_APPOINTMENT.format(appointment=message.text))
