from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from src.bot.logic.make_appointment.states import AppointmentStates


async def select_district(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int
) -> None:
    """
    Switch to the clinic selection
    """
    districts = manager.dialog_data["districts"]
    district = districts[item_id]
    manager.dialog_data["district"] = district

    await manager.switch_to(AppointmentStates.clinic)
