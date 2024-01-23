import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.common import sync_scroll
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import (
    Jinja, Format,
    List, Case,
    Const
)

from src.bot.logic.manage_tracking.states import TrackingStates
from src.bot.utils.buttons import get_menu_button
from .getter import data_getter
from .handlers import select_tracking

KB_HEIGHT = 4
KB_WIDTH = 3

LIST_ID = "tracking_list"
SCROLL_ID = "tracking_scroll"
SELECT_ID = "tracking_select"

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
            Format("{pos}"),
            items="user_tracking",
            item_id_getter=operator.attrgetter("id"),
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
