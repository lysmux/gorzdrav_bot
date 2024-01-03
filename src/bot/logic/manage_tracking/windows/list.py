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

from src.bot.logic.manage_tracking.states import TrackingStates
from src.bot.utils.aio_dialog import sync_scroll
from src.bot.utils.buttons import get_menu_button
from src.database.models import TrackingModel
from src.database.repositories import Repository

KB_HEIGHT = 4
KB_WIDTH = 3

WINDOW_NAME = "list_tracking"
LIST_ID = f"{WINDOW_NAME}_list"
SCROLL_ID = f"{WINDOW_NAME}_scroll"
SELECT_ID = f"{WINDOW_NAME}_select"


async def data_getter(
        repository: Repository,
        event_from_user: User,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
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


window = Window(
    Case(
        {
            False: Jinja("tracking/list_header.html"),
            True: Jinja("tracking/no_tracking.html"),
        },
        selector=F["user_tracking"].len() == 0
    ),
    Const(" "),
    List(
        Jinja("tracking/tracking_item.html"),
        sep="\n" * 2,
        items="user_tracking",
        id=LIST_ID,
        page_size=KB_WIDTH * KB_HEIGHT
    ),

    ScrollingGroup(
        Select(
            Format("{item[1].id}"),
            items="user_tracking",
            item_id_getter=operator.itemgetter(0),
            id=SELECT_ID,
            type_factory=int,
            on_click=select_tracking
        ),
        id=SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH,
        on_page_changed=sync_scroll(LIST_ID),
    ),
    get_menu_button(),

    getter=data_getter,
    state=TrackingStates.list,
)
