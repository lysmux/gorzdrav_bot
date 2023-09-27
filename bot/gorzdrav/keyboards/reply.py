from aiogram.utils.keyboard import ReplyKeyboardBuilder

from gorzdrav_api.schemas import District, Clinic, Speciality, Doctor, Appointment


def districts_keyboard_factory(districts: list[District]):
    keyboard = ReplyKeyboardBuilder()

    for district in districts:
        keyboard.button(text=district.name)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()


def clinics_keyboard_factory(clinics: list[Clinic]):
    keyboard = ReplyKeyboardBuilder()

    for clinic in clinics:
        keyboard.button(text=clinic.short_name)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()


def specialities_keyboard_factory(specialities: list[Speciality]):
    keyboard = ReplyKeyboardBuilder()

    for speciality in specialities:
        keyboard.button(text=speciality.name)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()


def doctors_keyboard_factory(doctors: list[Doctor]):
    keyboard = ReplyKeyboardBuilder()

    for doctor in doctors:
        keyboard.button(text=doctor.name)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()


def appointments_keyboard_factory(appointments: list[Appointment]):
    keyboard = ReplyKeyboardBuilder()

    for appointment in appointments:
        keyboard.button(text=appointment.time_str)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()
