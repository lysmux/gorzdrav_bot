from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.bot.services.appointments_checker import CheckerStorageProxy
from src.database import Repository
from src.database.models import TrackingModel


async def delete_tracking(
        callback: CallbackQuery,
        widget: Button,
        manager: DialogManager
) -> None:
    """
        Delete tracking from database
    """
    fsm_storage: BaseStorage = manager.middleware_data["fsm_storage"]
    repository: Repository = manager.middleware_data["repository"]
    tracking: TrackingModel = manager.dialog_data["selected_tracking"]

    checker_storage_proxy = CheckerStorageProxy(
        bot=callback.bot,
        storage=fsm_storage,
        tracking=tracking
    )

    await repository.tracking.delete(clause=TrackingModel.id == tracking.id)
    await checker_storage_proxy.remove()
