from typing import Any

from aiogram_dialog import DialogManager

from src.gorzdrav_api import GorZdravAPI
from src.gorzdrav_api.utils import generate_gorzdrav_url


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict[str, Any]:
    """
    Get appointments from API
    """

    district = dialog_manager.dialog_data["district"]
    clinic = dialog_manager.dialog_data["clinic"]
    speciality = dialog_manager.dialog_data["speciality"]
    doctor = dialog_manager.dialog_data["doctor"]

    appointments = await gorzdrav_api.get_appointments(
        clinic=clinic,
        doctor=doctor
    )
    appointment_url = generate_gorzdrav_url(
        district=district,
        clinic=clinic,
        speciality=speciality,
        doctor=doctor,
    )

    return {
        "appointments": (*enumerate(appointments),),
        "appointment_url": appointment_url
    }
