from typing import Any

from aiogram_dialog import DialogManager

from src.gorzdrav_api import GorZdravAPI


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict[str, Any]:
    """
    Get doctors from API
    """

    speciality = dialog_manager.dialog_data["speciality"]
    clinic = dialog_manager.dialog_data["clinic"]
    doctors = await gorzdrav_api.get_doctors(
        clinic=clinic,
        speciality=speciality
    )
    dialog_manager.dialog_data["doctors"] = doctors

    return {
        "doctors": (*enumerate(doctors),)
    }
