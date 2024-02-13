from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.bot.logic.dialogs.make_appointment.states import AppointmentStates

ROUTER_NAME = "make_appointment_handlers"

router = Router(name=ROUTER_NAME)


@router.message(Command("appointment"))
async def make_appointment(
        message: Message,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        AppointmentStates.district,
        mode=StartMode.RESET_STACK
    )
