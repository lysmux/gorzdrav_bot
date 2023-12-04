from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.bot.logic.gorzdrav.dialogs.appointment.states import AppointmentStates
from src.bot.logic.gorzdrav.dialogs.manage_tracking.states import TrackingStates

router = Router()


@router.message(Command("appointment"))
async def make_appointment(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AppointmentStates.district, mode=StartMode.RESET_STACK)


@router.message(Command("tracking"))
async def tracking(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(TrackingStates.list, mode=StartMode.RESET_STACK)
