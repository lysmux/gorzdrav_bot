import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Jinja

from bot.gorzdrav.dialogs.appointment.states import AppointmentStates
from bot.misc.buttons import MENU_BUTTON
from gorzdrav_api.api import GorZdravAPI

KB_HEIGHT = 4
KB_WIDTH = 2

WINDOW_NAME = "districts"
KEYBOARD_SCROLL_ID = f"{WINDOW_NAME}_kb_scroll"
SELECT_ID = f"{WINDOW_NAME}_select"


async def districts_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
    districts = await gorzdrav_api.get_districts()
    dialog_manager.dialog_data["districts"] = districts

    return {
        "districts": (*enumerate(districts),)
    }


async def district_handler(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int
):
    districts = manager.dialog_data["districts"]
    district = districts[item_id]
    manager.dialog_data["district"] = district

    await manager.switch_to(AppointmentStates.clinic)


window = Window(
    Jinja("gorzdrav/appointment/district/header.html"),
    ScrollingGroup(
        Select(
            text=Format("{item[1].name}"),
            id=SELECT_ID,
            items="districts",
            item_id_getter=operator.itemgetter(0),
            type_factory=int,
            on_click=district_handler
        ),
        id=KEYBOARD_SCROLL_ID,
        width=KB_WIDTH,
        height=KB_HEIGHT,
    ),
    MENU_BUTTON,
    state=AppointmentStates.district,
    getter=districts_getter
)
