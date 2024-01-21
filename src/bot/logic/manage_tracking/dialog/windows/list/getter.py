from typing import Any

from aiogram.types import User
from aiogram_dialog import DialogManager

from src.database import Repository
from src.database.models import TrackingModel


async def data_getter(
        repository: Repository,
        event_from_user: User,
        dialog_manager: DialogManager,
        **kwargs
) -> dict[str, Any]:
    """
        Get user tracking from database
    """
    user_tracking = await repository.tracking.get_all(
        clause=TrackingModel.user.has(tg_id=event_from_user.id),
        order_by=(TrackingModel.clinic, TrackingModel.doctor)
    )
    dialog_manager.dialog_data["user_tracking"] = user_tracking

    return {
        "user_tracking": (*enumerate(user_tracking),)
    }
