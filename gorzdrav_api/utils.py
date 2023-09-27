import json
from urllib.parse import quote


def generate_gorzdrav_url(district: str,
                             clinic: str,
                             speciality: str,
                             doctor: str) -> str:
    base_url = "https://gorzdrav.spb.ru/service-free-schedule#"

    params = [
        {"district": district},
        {"lpu": clinic},
        {"speciality": speciality},
        {"doctor": doctor},
    ]

    params = json.dumps(params, separators=(",", ":"))
    params = quote(params, safe="/,+:=")

    return base_url + params
