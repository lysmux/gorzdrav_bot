from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.bot.logic.manage_tracking.states import TrackingStates
from src.database import Repository
from src.database.models import TrackingModel, UserModel
from src.services.appointments_checker import StorageProxy


async def delete_tracking(
        callback: CallbackQuery,
        widget: Button,
        manager: DialogManager
) -> None:
    """
        Delete tracking from database
    """
    repository: Repository = manager.middleware_data["repository"]
    storage_proxy: StorageProxy = manager.middleware_data["storage_proxy"]
    user: UserModel = manager.middleware_data["user"]
    tracking_id: int = manager.dialog_data["selected_tracking"]

    await storage_proxy.clear()
    await repository.tracking.delete(clause=(
        TrackingModel.id == tracking_id,
        TrackingModel.user == user
    ))

    await manager.switch_to(TrackingStates.deleted)
