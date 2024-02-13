from typing import Any

from aiogram_dialog import DialogManager

from src.gorzdrav_api import GorZdravAPI


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict[str, Any]:
    """
    Get districts from API
    """
    districts = await gorzdrav_api.get_districts()
    dialog_manager.dialog_data["districts"] = districts

    return {
        "districts": (*enumerate(districts),)
    }
