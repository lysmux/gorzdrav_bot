from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.bot.logic.dialogs.manage_tracking.states import TrackingStates
from src.database import Repository
from src.database.models import TrackingModel, UserModel


async def delete_tracking(
        callback: CallbackQuery,
        widget: Button,
        manager: DialogManager
) -> None:
    """
        Delete tracking from database
    """
    repository: Repository = manager.middleware_data["repository"]
    user: UserModel = manager.middleware_data["user"]
    tracking_id: int = manager.dialog_data["selected_tracking"]

    await repository.tracking.delete(clause=(
        TrackingModel.id == tracking_id,
        TrackingModel.user == user
    ))

    await manager.switch_to(TrackingStates.deleted)
