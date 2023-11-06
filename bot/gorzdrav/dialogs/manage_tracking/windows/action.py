from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, SwitchTo
from aiogram_dialog.widgets.text import Jinja, Const

from bot.gorzdrav.dialogs.manage_tracking import button_texts
from bot.gorzdrav.dialogs.manage_tracking.states import TrackingStates
from bot.misc.buttons import back_button
from database.database import Repository
from database.models.tracking import Tracking

STATUS_BTN_ID = "status_btn"
DELETE_BTN_ID = "delete_btn"


async def tracking_delete_handler(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager
):
    repository: Repository = manager.middleware_data["repository"]
    tracking: Tracking = manager.dialog_data["tracking"]

    await repository.delete_tracking(tracking_id=tracking.id)


window = Window(
    Jinja("gorzdrav/tracking/tracking/action.html"),
    Group(
        SwitchTo(
            Const(button_texts.STATUS),
            id=STATUS_BTN_ID,
            state=TrackingStates.status
        ),
        SwitchTo(
            Const(button_texts.DELETE),
            id=DELETE_BTN_ID,
            state=TrackingStates.deleted,
            on_click=tracking_delete_handler
        ),
        width=2
    ),
    back_button(state=TrackingStates.list),
    state=TrackingStates.action
)
