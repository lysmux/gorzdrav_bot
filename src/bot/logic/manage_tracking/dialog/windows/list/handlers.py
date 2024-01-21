from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from src.bot.logic.manage_tracking.states import TrackingStates


async def select_tracking(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int,
) -> None:
    """
        Switch to the action selection
    """
    user_tracking = manager.dialog_data["user_tracking"]
    selected_tracking = user_tracking[item_id]
    manager.dialog_data["selected_tracking"] = selected_tracking

    await manager.switch_to(TrackingStates.action)
