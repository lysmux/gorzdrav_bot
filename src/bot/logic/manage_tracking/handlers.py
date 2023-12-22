from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.bot.logic.manage_tracking.states import TrackingStates

router = Router()


@router.message(Command("tracking"))
async def tracking(
        message: Message,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        TrackingStates.list,
        mode=StartMode.RESET_STACK
    )
