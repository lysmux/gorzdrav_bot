from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from src.bot.logic.manage_tracking.states import TrackingStates


async def select_tracking(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        tracking_id: int,
) -> None:
    """
        Switch to the action selection
    """
    manager.dialog_data["selected_tracking"] = tracking_id

    await manager.switch_to(TrackingStates.action)
