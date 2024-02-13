from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from src.bot.logic.dialogs.general.states import GeneralStates

ROUTER_NAME = "dialog_errors"

router = Router(name=ROUTER_NAME)


@router.error(ExceptionTypeFilter(UnknownIntent))
async def unknown_intent_handler(event: ErrorEvent) -> None:
    """
    Handle unknown intent error. Delete message
    """
    match event.update.event:
        case CallbackQuery() as call:
            await call.message.delete()
        case Message() as message:
            await message.delete()


@router.error(ExceptionTypeFilter(UnknownState))
async def unknown_state_handler(
        event: ErrorEvent,
        dialog_manager: DialogManager
) -> None:
    """
    Handle unknown state error. Switch to menu
    """
    await dialog_manager.start(
        state=GeneralStates.menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND
    )
