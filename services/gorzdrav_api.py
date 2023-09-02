import datetime
import urllib.parse

import aiohttp as aiohttp

from models.gorzdrav import District, Clinic, Speciality, Doctor, Appointment

API_URL = "https://gorzdrav.spb.ru/_api/api/v2"
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/103.0.0.0 Safari/537.36",
}


async def get_districts() -> list[District]:
    result = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{API_URL}/shared/districts", headers=HEADERS) as response:
            r_json = await response.json()
            for response_item in r_json["result"]:
                result.append(District(response_item["id"], response_item["name"].strip()))
    return result


async def get_clinics(district: District) -> list[Clinic]:
    result = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{API_URL}/shared/district/{district.id}/lpus", headers=HEADERS) as response:
            r_json = await response.json()
            for response_item in r_json["result"]:
                result.append(Clinic(response_item["id"], response_item["lpuShortName"].strip()))
    return result


async def get_specialities(clinic: Clinic) -> list[Speciality]:
    result = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{API_URL}/schedule/lpu/{clinic.id}/specialties", headers=HEADERS) as response:
            r_json = await response.json()
            for response_item in r_json["result"]:
                result.append(
                    Speciality(urllib.parse.quote(response_item["id"], safe=""), response_item["name"].strip()))
    return result


async def get_doctors(clinic: Clinic, speciality: Speciality) -> list[Doctor]:
    result = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{API_URL}/schedule/lpu/{clinic.id}/speciality/{speciality.id}/doctors",
                               headers=HEADERS) as response:
            r_json = await response.json()
            for response_item in r_json["result"]:
                result.append(Doctor(urllib.parse.quote(response_item["id"], safe=""), response_item["name"].strip()))
    return result


async def get_appointments(clinic: Clinic, doctor: Doctor) -> list[Appointment]:
    result = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{API_URL}/schedule/lpu/{clinic.id}/doctor/{doctor.id}/appointments",
                               headers=HEADERS) as response:
            r_json = await response.json()
            if r_json["success"]:
                for response_item in r_json["result"]:
                    a_datetime = datetime.datetime.fromisoformat(response_item["visitStart"])
                    result.append(Appointment(response_item["id"], a_datetime))
    return result
