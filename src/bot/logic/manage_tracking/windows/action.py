from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Button
from aiogram_dialog.widgets.text import Jinja, Const

from src.bot import keyboard_texts
from src.bot.logic.manage_tracking.states import TrackingStates
from src.bot.services.appointments_checker import CheckerStorageProxy
from src.bot.utils.buttons import get_back_button
from src.database.models import TrackingModel
from src.database.repositories import Repository

WINDOW_NAME = "tracking_action"
STATUS_BTN_ID = f"{WINDOW_NAME}_status_btn"
DELETE_BTN_ID = f"{WINDOW_NAME}_delete_btn"


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


window = Window(
    Jinja("tracking/action_header.html"),
    Group(
        SwitchTo(
            Const(keyboard_texts.tracking.STATUS),
            id=STATUS_BTN_ID,
            state=TrackingStates.status
        ),
        SwitchTo(
            Const(keyboard_texts.tracking.DELETE),
            id=DELETE_BTN_ID,
            state=TrackingStates.deleted,
            on_click=delete_tracking
        ),
        width=2
    ),
    get_back_button(TrackingStates.list),
    state=TrackingStates.action
)
