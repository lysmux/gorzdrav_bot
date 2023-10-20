from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from bot.gorzdrav.keyboards import inline, paginator_items
from bot.gorzdrav.keyboards.callbacks import ItemCallback
from bot.gorzdrav.states import AppointmentStates
from bot.middlewares.gorzdrav_api import GorZdravAPIMiddleware
from bot.utils.inline_paginator import Paginator
from bot.utils.template_engine import render_template
from gorzdrav_api.api import GorZdravAPI

router = Router()

router.message.middleware(GorZdravAPIMiddleware())
router.callback_query.middleware(GorZdravAPIMiddleware())
router.callback_query.middleware(CallbackAnswerMiddleware())


@router.message(Command("make_appointment"))
async def make_appointment_handler(
        message: types.Message,
        state: FSMContext,
        gorzdrav_api: GorZdravAPI
):
    districts = await gorzdrav_api.get_districts()
    items = paginator_items.districts_items_factory(districts)

    paginator = Paginator(
        router=router,
        name="districts",
        header_text=render_template("gorzdrav/appointment/districts_header.html"),
        items=items
    )

    await state.set_state(AppointmentStates.district)
    await state.update_data(districts=districts)
    await paginator.send_paginator(message)


@router.callback_query(
    AppointmentStates.district,
    ItemCallback.filter()
)
async def district_handler(
        call: types.CallbackQuery,
        callback_data: ItemCallback,
        state: FSMContext,
        gorzdrav_api: GorZdravAPI
):
    districts = (await state.get_data()).get("districts")
    district = next(filter(lambda x: x.id == callback_data.id, districts))

    clinics = await gorzdrav_api.get_clinics(district)
    items = paginator_items.clinics_items_factory(clinics)

    paginator = Paginator(
        router=router,
        name="clinics",
        header_text=render_template("gorzdrav/appointment/clinics_header.html"),
        items=items
    )

    await state.set_state(AppointmentStates.clinic)
    await state.update_data(clinics=clinics, district=district)
    await paginator.update_paginator(call)


@router.callback_query(
    AppointmentStates.clinic,
    ItemCallback.filter()
)
async def clinic_handler(
        call: types.CallbackQuery,
        callback_data: ItemCallback,
        state: FSMContext,
        gorzdrav_api: GorZdravAPI
):
    clinics = (await state.get_data()).get("clinics")
    clinic = next(filter(lambda x: x.id == callback_data.id, clinics))

    specialities = await gorzdrav_api.get_specialities(clinic)
    items = paginator_items.specialities_items_factory(specialities)

    paginator = Paginator(
        router=router,
        name="specialities",
        header_text=render_template("gorzdrav/appointment/specialities_header.html"),
        items=items
    )

    await state.set_state(AppointmentStates.speciality)
    await state.update_data(specialities=specialities, clinic=clinic)
    await paginator.update_paginator(call)


@router.callback_query(
    AppointmentStates.speciality,
    ItemCallback.filter()
)
async def speciality_handler(
        call: types.CallbackQuery,
        callback_data: ItemCallback,
        state: FSMContext,
        gorzdrav_api: GorZdravAPI
):
    state_data = await state.get_data()
    specialities = state_data.get("specialities")
    clinic = state_data.get("clinic")
    speciality = next(filter(lambda x: x.id == callback_data.id, specialities))

    doctors = await gorzdrav_api.get_doctors(clinic, speciality)
    items = paginator_items.doctors_items_factory(doctors)

    paginator = Paginator(
        router=router,
        name="doctors",
        header_text=render_template("gorzdrav/appointment/doctors_header.html"),
        items=items
    )

    await state.set_state(AppointmentStates.doctor)
    await state.update_data(doctors=doctors, speciality=speciality)
    await paginator.update_paginator(call)


@router.callback_query(
    AppointmentStates.doctor,
    ItemCallback.filter()
)
async def doctor_handler(
        call: types.CallbackQuery,
        callback_data: ItemCallback,
        state: FSMContext,
        gorzdrav_api: GorZdravAPI
):
    state_data = await state.get_data()
    district = state_data.get("district")
    clinic = state_data.get("clinic")
    speciality = state_data.get("speciality")
    doctors = state_data.get("doctors")
    doctor = next(filter(lambda x: x.id == callback_data.id, doctors))

    markup = inline.add_tracking_mp()

    appointments = await gorzdrav_api.get_appointments(clinic, doctor)
    if appointments:
        items = paginator_items.appointments_items_factory(
            district=district,
            clinic=clinic,
            speciality=speciality,
            doctor=doctor,
            appointments=appointments
        )
        paginator = Paginator(
            router=router,
            name="appointments",
            header_text=render_template("gorzdrav/appointment/appointments_header.html"),
            items=items,
            static_markup=markup
        )

        await paginator.update_paginator(call)
    else:
        await call.message.edit_text(
            text=render_template("gorzdrav/appointment/no_appointments.html"),
            reply_markup=markup)

    await state.update_data(doctor=doctor)
    await state.set_state(AppointmentStates.appointment)
