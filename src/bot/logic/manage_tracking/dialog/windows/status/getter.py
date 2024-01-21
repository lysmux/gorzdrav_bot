from typing import Any

from aiogram_dialog import DialogManager

from src.database.models import TrackingModel
from src.gorzdrav_api import GorZdravAPI
from src.gorzdrav_api.utils import filter_appointments, generate_gorzdrav_url


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict[str, Any]:
    tracking: TrackingModel = dialog_manager.dialog_data["selected_tracking"]
    appointments = await gorzdrav_api.get_appointments(
        clinic=tracking.clinic,
        doctor=tracking.doctor
    )
    filtered_appointments = filter_appointments(
        appointments=appointments,
        hours=tracking.hours
    )

    appointment_url = generate_gorzdrav_url(
        district=tracking.district,
        clinic=tracking.clinic,
        speciality=tracking.speciality,
        doctor=tracking.doctor,
    )

    return {
        "tracking": tracking,
        "filtered_appointments": (*enumerate(filtered_appointments),),
        "appointment_url": appointment_url
    }
