from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from src.bot.logic.dialogs.manage_tracking.states import TrackingStates
from src.services.appointments_checker.checker import TrackingCallback

ROUTER_NAME = "manage_tracking_handlers"

router = Router(name=ROUTER_NAME)


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
    await call.bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=dialog_manager.current_stack().last_message_id
    )

    await dialog_manager.start(
        TrackingStates.status,
        mode=StartMode.RESET_STACK,
        data={"selected_tracking": callback_data.id}
    )
