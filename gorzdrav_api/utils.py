import json
from urllib.parse import quote

from gorzdrav_api.schemas import District, Clinic, Speciality, Doctor


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
