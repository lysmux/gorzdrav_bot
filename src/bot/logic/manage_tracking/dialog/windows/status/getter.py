from typing import Any

from aiogram_dialog import DialogManager

from src.database import Repository
from src.database.models import TrackingModel
from src.gorzdrav_api import GorZdravAPI
from src.gorzdrav_api.utils import filter_appointments, generate_gorzdrav_url


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        repository: Repository,
        **kwargs
) -> dict[str, Any]:
    tracking_id: int = dialog_manager.dialog_data["selected_tracking"]
    tracking = await repository.tracking.get(clause=TrackingModel.id == tracking_id)

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
        "filtered_appointments": filtered_appointments,
        "appointment_url": appointment_url
    }
