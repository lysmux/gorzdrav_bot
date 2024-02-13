from typing import Any

from aiogram_dialog import DialogManager

from src.gorzdrav_api import GorZdravAPI


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict[str, Any]:
    """
    Get clinics from API
    """
    district = dialog_manager.dialog_data["district"]
    clinics = await gorzdrav_api.get_clinics(district=district)
    dialog_manager.dialog_data["clinics"] = clinics

    return {
        "clinics": (*enumerate(clinics),)
    }
