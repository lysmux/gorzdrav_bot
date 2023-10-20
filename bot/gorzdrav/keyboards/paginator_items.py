from typing import Iterable

from aiogram.types import InlineKeyboardButton

from bot.gorzdrav.keyboards import callbacks
from bot.utils.inline_paginator import PaginatorItem
from bot.utils.template_engine import render_template
from database.models.tracking import Tracking
from gorzdrav_api.schemas import District, Clinic, Speciality, Doctor, Appointment
from gorzdrav_api.utils import generate_gorzdrav_url


def tracking_items_factory(user_tracking: Iterable[Tracking]) -> list[PaginatorItem]:
    items = [
        PaginatorItem(
            text=render_template("gorzdrav/tracking/tracking_item.html", tracking=tracking),
            button=InlineKeyboardButton(
                text=str(tracking.id),
                callback_data=callbacks.TrackingCallback(id=tracking.id).pack()
            )
        ) for tracking in user_tracking
    ]

    return items


def districts_items_factory(districts: Iterable[District]) -> list[PaginatorItem]:
    items = [
        PaginatorItem(
            button=InlineKeyboardButton(
                text=district.name,
                callback_data=callbacks.ItemCallback(id=district.id).pack()
            )
        ) for district in districts
    ]

    return items


def clinics_items_factory(clinics: Iterable[Clinic]) -> list[PaginatorItem]:
    items = [
        PaginatorItem(
            text=render_template("gorzdrav/appointment/clinic_item.html", clinic=clinic),
            button=InlineKeyboardButton(
                text=clinic.short_name,
                callback_data=callbacks.ItemCallback(id=clinic.id).pack()
            )
        ) for clinic in clinics
    ]

    return items


def specialities_items_factory(specialities: Iterable[Speciality]) -> list[PaginatorItem]:
    items = [
        PaginatorItem(
            button=InlineKeyboardButton(
                text=speciality.name,
                callback_data=callbacks.ItemCallback(id=speciality.id).pack()
            )
        ) for speciality in specialities
    ]

    return items


def doctors_items_factory(doctors: Iterable[Doctor]) -> list[PaginatorItem]:
    items = [
        PaginatorItem(
            text=render_template("gorzdrav/appointment/doctor_item.html", doctor=doctor),
            button=InlineKeyboardButton(
                text=doctor.short_name,
                callback_data=callbacks.ItemCallback(id=doctor.id).pack()
            )
        ) for doctor in doctors
    ]

    return items


def appointments_items_factory(
        district: District,
        clinic: Clinic,
        speciality: Speciality,
        doctor: Doctor,
        appointments: Iterable[Appointment]
) -> list[PaginatorItem]:
    url = generate_gorzdrav_url(
        district=district,
        clinic=clinic,
        speciality=speciality,
        doctor=doctor,
    )

    items = [
        PaginatorItem(
            button=InlineKeyboardButton(
                text=appointment.time_str,
                url=url
            )
        ) for appointment in appointments
    ]

    return items
