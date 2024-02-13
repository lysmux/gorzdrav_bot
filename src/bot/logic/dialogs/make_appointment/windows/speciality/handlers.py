from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from src.bot.logic.dialogs.make_appointment.states import AppointmentStates


async def select_speciality(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int
):
    """
    Switch to the doctor selection
    """

    specialities = manager.dialog_data["specialities"]
    speciality = specialities[item_id]
    manager.dialog_data["speciality"] = speciality

    await manager.switch_to(AppointmentStates.doctor)
