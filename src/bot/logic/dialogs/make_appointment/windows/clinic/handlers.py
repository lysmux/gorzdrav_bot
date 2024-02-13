from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from src.bot.logic.dialogs.make_appointment.states import AppointmentStates


async def select_clinic(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int
) -> None:
    """
    Switch to the speciality selection
    """

    clinics = manager.dialog_data["clinics"]
    clinic = clinics[item_id]
    manager.dialog_data["clinic"] = clinic

    await manager.switch_to(AppointmentStates.speciality)
