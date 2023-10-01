from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.gorzdrav.keyboards import reply, inline
from bot.gorzdrav.states import AppointmentStates
from bot.middlewares.gorzdrav_api import GorZdravAPIMiddleware
from bot.utils.template_engine import render_template
from gorzdrav_api.api import GorZdravAPI

router = Router()
router.message.middleware(GorZdravAPIMiddleware())


@router.message(Command("make_appointment"))
async def make_appointment_handler(message: types.Message, state: FSMContext, gorzdrav_api: GorZdravAPI):
    districts = await gorzdrav_api.get_districts()
    keyboard = reply.districts_keyboard_factory(districts)

    await state.set_state(AppointmentStates.district)
    await state.update_data(districts=districts)
    await message.answer(text=render_template("gorzdrav/appointment/districts.html"), reply_markup=keyboard)


@router.message(AppointmentStates.district)
async def district_handler(message: types.Message, state: FSMContext, gorzdrav_api: GorZdravAPI):
    districts = (await state.get_data())["districts"]
    selected_district = next(filter(lambda x: x.name == message.text, districts), None)

    if selected_district:
        clinics = await gorzdrav_api.get_clinics(selected_district)
        keyboard = reply.clinics_keyboard_factory(clinics)
        await state.set_state(AppointmentStates.clinic)
        await state.update_data(clinics=clinics, selected_district=selected_district)
        await message.answer(text=render_template("gorzdrav/appointment/clinics.html", clinics=clinics),
                             reply_markup=keyboard)
    else:
        await message.answer(text=render_template("gorzdrav/appointment/unknown_district.html", district=message.text))


@router.message(AppointmentStates.clinic)
async def clinic_handler(message: types.Message, state: FSMContext, gorzdrav_api: GorZdravAPI):
    clinics = (await state.get_data())["clinics"]
    selected_clinic = next(filter(lambda x: x.short_name == message.text, clinics), None)

    if selected_clinic:
        specialities = await gorzdrav_api.get_specialities(selected_clinic)
        keyboard = reply.specialities_keyboard_factory(specialities)
        await state.set_state(AppointmentStates.speciality)
        await state.update_data(specialities=specialities, selected_clinic=selected_clinic)
        await message.answer(text=render_template("gorzdrav/appointment/specialities.html"), reply_markup=keyboard)
    else:
        await message.answer(text=render_template("gorzdrav/appointment/unknown_clinic.html", clinic=message.text))


@router.message(AppointmentStates.speciality)
async def speciality_handler(message: types.Message, state: FSMContext, gorzdrav_api: GorZdravAPI):
    state_data = await state.get_data()
    specialities = state_data["specialities"]
    selected_clinic = state_data["selected_clinic"]
    selected_speciality = next(filter(lambda x: x.name == message.text, specialities), None)

    if selected_speciality:
        doctors = await gorzdrav_api.get_doctors(selected_clinic, selected_speciality)
        keyboard = reply.doctors_keyboard_factory(doctors)
        await state.set_state(AppointmentStates.doctor)
        await state.update_data(doctors=doctors, selected_speciality=selected_speciality)
        await message.answer(text=render_template("gorzdrav/appointment/doctors.html", doctors=doctors),
                             reply_markup=keyboard)
    else:
        await message.answer(
            text=render_template("gorzdrav/appointment/unknown_speciality.html", speciality=message.text))


@router.message(AppointmentStates.doctor)
async def doctor_handler(message: types.Message, state: FSMContext, gorzdrav_api: GorZdravAPI):
    state_data = await state.get_data()
    doctors = state_data["doctors"]
    selected_clinic = state_data["selected_clinic"]
    selected_doctor = next(filter(lambda x: x.name == message.text, doctors), None)

    if selected_doctor:
        appointments = await gorzdrav_api.get_appointments(selected_clinic, selected_doctor)
        if appointments:
            keyboard = reply.appointments_keyboard_factory(appointments)
            await state.update_data(appointments=appointments)
            await message.answer(text=render_template("gorzdrav/appointment/appointments.html", doctors=doctors),
                                 reply_markup=keyboard)

        action_keyboard = inline.monitor_keyboard_factory()
        await message.answer(
            text=render_template("gorzdrav/tracking/add_tracking.html", no_appointments=not bool(appointments)),
            reply_markup=action_keyboard)
        await state.update_data(selected_doctor=selected_doctor)
        await state.set_state(AppointmentStates.appointment)
    else:
        await message.answer(text=render_template("gorzdrav/appointment/unknown_doctor.html", doctor=message.text))
