from typing import TypeVar, cast
from urllib.parse import quote

from aiohttp import ClientSession, client_exceptions, ContentTypeError
from cashews import cache
from pydantic import BaseModel, TypeAdapter

from gorzdrav_api.exceptions import ServerError, ResponseParseError
from gorzdrav_api.schemas import District, Clinic, Speciality, Doctor, Appointment

cache.setup("mem://")

P = TypeVar("P", bound=BaseModel)


class GorZdravAPI:
    API_URL = "https://gorzdrav.spb.ru/_api/api/v2"
    HEADERS = {
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/103.0.0.0 Safari/537.36",
    }

    def __init__(self):
        self._http_client = ClientSession()

    async def make_request(
            self,
            method: str,
            url_part: str,
            response_model: type[list[BaseModel] | BaseModel],
            params: dict[str, str] | None = None,
    ) -> P | list[P] | None:
        try:
            response = await self._http_client.request(
                method,
                f"{self.API_URL}/{url_part}",
                params=params,
                headers=self.HEADERS,
                ssl=False,
            )
        except (client_exceptions.ClientConnectionError, client_exceptions.ClientConnectorError) as e:
            raise ServerError(f"Connection error, details: {e}")

        if response.status != 200:
            details = await response.text()
            raise ServerError(f"Server returned {response.status}, details: {details}")

        try:
            deserialized_data = await response.json()
        except ContentTypeError as e:
            raise ResponseParseError(
                e.message,
            )

        if deserialized_data["success"]:
            ta = TypeAdapter(response_model)
            return cast(response_model, ta.validate_python(deserialized_data["result"]))
        else:
            return None

    @cache.soft(ttl="24h", soft_ttl="3h")
    async def get_districts(self) -> list[District]:
        return await self.make_request(
            method="GET",
            url_part="shared/districts",
            response_model=list[District]
        )

    @cache.soft(ttl="24h", soft_ttl="3h")
    async def get_clinics(self, district: District) -> list[Clinic]:
        return await self.make_request(
            method="GET",
            url_part=f"shared/district/{district.id}/lpus",
            response_model=list[Clinic]
        )

    @cache.soft(ttl="24h", soft_ttl="3h")
    async def get_specialities(self, clinic: Clinic) -> list[Speciality]:
        return await self.make_request(
            method="GET",
            url_part=f"schedule/lpu/{clinic.id}/specialties",
            response_model=list[Speciality]
        )

    async def get_doctors(self, clinic: Clinic, speciality: Speciality) -> list[Doctor]:
        speciality_id = quote(speciality.id, safe="")

        return await self.make_request(
            method="GET",
            url_part=f"schedule/lpu/{clinic.id}/speciality/{speciality_id}/doctors",
            response_model=list[Doctor]
        )

    async def get_appointments(self, clinic: Clinic, doctor: Doctor) -> list[Appointment]:
        return await self.make_request(
            method="GET",
            url_part=f"schedule/lpu/{clinic.id}/doctor/{doctor.id}/appointments",
            response_model=list[Appointment]
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._http_client.close()
