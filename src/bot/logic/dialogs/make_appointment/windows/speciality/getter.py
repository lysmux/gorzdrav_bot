from typing import Any

from aiogram_dialog import DialogManager

from src.gorzdrav_api import GorZdravAPI


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict[str, Any]:
    """
    Get specialities from API
    """

    clinic = dialog_manager.dialog_data["clinic"]
    specialities = await gorzdrav_api.get_specialities(clinic=clinic)
    dialog_manager.dialog_data["specialities"] = specialities

    return {
        "specialities": (*enumerate(specialities),)
    }
