from typing import Any

from aiogram_dialog import DialogManager

from src.database import Repository
from src.database.models import TrackingModel
from src.gorzdrav_api import GorZdravAPI
from src.gorzdrav_api.utils import generate_gorzdrav_url


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        repository: Repository,
        **kwargs
) -> dict[str, Any]:
    if selected_tracking := dialog_manager.start_data.get("selected_tracking"):
        tracking_id: int = selected_tracking
    else:
        tracking_id: int = dialog_manager.dialog_data["selected_tracking"]

    tracking = await repository.tracking.get(
        clause=TrackingModel.id == tracking_id
    )
    appointment_url = generate_gorzdrav_url(
        district=tracking.district,
        clinic=tracking.clinic,
        speciality=tracking.speciality,
        doctor=tracking.doctor,
    )

    if tracking:
        appointments = await gorzdrav_api.get_appointments(
            clinic=tracking.clinic,
            doctor=tracking.doctor
        )

        if appointments:
            return {
                "tracking": tracking,
                "appointments": appointments,
                "appointment_url": appointment_url
            }
        return {
            "error": "no_appointments"
        }

    return {
        "error": "not_exists",
    }
