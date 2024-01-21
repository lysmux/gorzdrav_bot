from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from src.bot.logic.make_appointment.states import AppointmentStates


async def select_doctor(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int
):
    """
    Switch to the appointment selection
    """

    doctors = manager.dialog_data["doctors"]
    doctor = doctors[item_id]
    manager.dialog_data["doctor"] = doctor

    await manager.switch_to(AppointmentStates.appointment)
