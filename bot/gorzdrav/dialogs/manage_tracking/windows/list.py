import operator

from aiogram import F
from aiogram.types import User, CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import (
    Jinja,
    Format,
    List,
    Case,
    Const
)

from bot.gorzdrav.dialogs.manage_tracking.states import TrackingStates
from bot.misc.buttons import MENU_BUTTON
from bot.utils.aio_dialog import sync_scroll
from database.database import Repository

KB_HEIGHT = 4
KB_WIDTH = 3

WINDOW_NAME = "list_tracking"
LIST_SCROLL_ID = f"{WINDOW_NAME}_list_scroll"
KEYBOARD_SCROLL_ID = f"{WINDOW_NAME}_kb_scroll"
SELECT_ID = f"{WINDOW_NAME}_select"


async def tracking_getter(
        repository: Repository,
        event_from_user: User,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
    user_tracking = await repository.get_user_tracking(tg_user_id=event_from_user.id)
    user_tracking = list(user_tracking)
    dialog_manager.dialog_data["user_tracking"] = user_tracking

    return {
        "user_tracking": (*enumerate(user_tracking),)
    }


async def tracking_handler(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int,
):
    user_tracking = manager.dialog_data["user_tracking"]
    tracking = user_tracking[item_id]
    manager.dialog_data["tracking"] = tracking

    await manager.switch_to(TrackingStates.action)


window = Window(
    Case(
        {
            False: Jinja("gorzdrav/tracking/tracking/header.html"),
            True: Jinja("gorzdrav/tracking/tracking/no_tracking.html"),
        },
        selector=F["user_tracking"].len() == 0
    ),
    Const(" "),
    List(
        Jinja("gorzdrav/tracking/tracking/item.html"),
        sep="\n" * 2,
        items="user_tracking",
        id=LIST_SCROLL_ID,
        page_size=KB_WIDTH * KB_HEIGHT
    ),
    ScrollingGroup(
        Select(
            Format("{item[1].id}"),
            items="user_tracking",
            item_id_getter=operator.itemgetter(0),
            id=SELECT_ID,
            type_factory=int,
            on_click=tracking_handler
        ),
        id=KEYBOARD_SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH,
        on_page_changed=sync_scroll(LIST_SCROLL_ID),
    ),
    MENU_BUTTON,
    state=TrackingStates.list,
    getter=tracking_getter
)
