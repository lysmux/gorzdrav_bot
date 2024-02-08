import json
from typing import Sequence
from urllib.parse import quote

from .schemas import (
    District, Clinic,
    Speciality, Doctor,
    Appointment
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

    str_params = json.dumps(params, separators=(",", ":"))
    str_params = quote(str_params, safe="/,+:=")

    return base_url + str_params


def filter_appointments(
        appointments: Sequence[Appointment],
        hours: set[int]
) -> tuple[Appointment, ...]:
    filtered_appointments = tuple(filter(
        lambda x: x.time.hour in hours, appointments
    ))

    return filtered_appointments
