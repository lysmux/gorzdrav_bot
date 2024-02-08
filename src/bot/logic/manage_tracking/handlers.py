from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from src.services.appointments_checker.checker import TrackingCallback
from .states import TrackingStates

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


@router.callback_query(TrackingCallback.filter())
async def notify(
        call: CallbackQuery,
        callback_data: TrackingCallback,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        TrackingStates.status,
        mode=StartMode.RESET_STACK,
        data={"selected_tracking": callback_data.id}
    )
