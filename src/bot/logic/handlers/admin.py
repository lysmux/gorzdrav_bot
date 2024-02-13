from aiogram import Router, F
from aiogram.filters import Command, MagicData
from aiogram.types import Message
from aiogram_dialog import StartMode, DialogManager

from src.bot.logic.dialogs.admin.states import AdminStates

ROUTER_NAME = "admin_handlers"

router = Router(name=ROUTER_NAME)
router.message.filter(
    MagicData(F["user_is_admin"].is_(True))
)


@router.message(Command("admin"))
async def admin_handler(
        message: Message,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        AdminStates.action,
        mode=StartMode.RESET_STACK
    )
