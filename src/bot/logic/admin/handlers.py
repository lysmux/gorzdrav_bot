from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import StartMode, DialogManager

from .states import AdminStates

router = Router()


@router.message(Command("admin"))
async def admin_handler(
        message: Message,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        AdminStates.action,
        mode=StartMode.RESET_STACK
    )
