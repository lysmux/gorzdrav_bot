import json
from itertools import chain
from urllib.parse import quote

from .schemas import (
    District, Clinic, Speciality, Doctor, Appointment
)


def generate_gorzdrav_url(
        district: District,
        clinic: Clinic,
        speciality: Speciality,
        doctor: Doctor
) -> str:
    base_url = "https://gorzdrav.spb.ru/service-free-schedule#"

    params = [
        {"district": district.id},
        {"lpu": clinic.id},
        {"speciality": speciality.id},
        {"doctor": doctor.id},
    ]

    params = json.dumps(params, separators=(",", ":"))
    params = quote(params, safe="/,+:=")

    return base_url + params


def filter_appointments(
        appointments: list[Appointment],
        hours: set[int]
) -> list[Appointment]:
    filtered_appointments = list(filter(
        lambda x: x.time.hour in hours, appointments
    ))

    return filtered_appointments
