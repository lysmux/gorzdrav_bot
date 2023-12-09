import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Jinja

from bot.utils.buttons import get_menu_button
from gorzdrav_api import GorZdravAPI
from ..states import AppointmentStates

KB_HEIGHT = 4
KB_WIDTH = 2

WINDOW_NAME = "districts"
SCROLL_ID = f"{WINDOW_NAME}_scroll"
SELECT_ID = f"{WINDOW_NAME}_select"


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
    """
    Get districts from API
    """
    districts = await gorzdrav_api.get_districts()
    dialog_manager.dialog_data["districts"] = districts

    return {
        "districts": (*enumerate(districts),)
    }


async def select_district(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int
) -> None:
    """
    Switch to the clinic selection
    """
    districts = manager.dialog_data["districts"]
    district = districts[item_id]
    manager.dialog_data["district"] = district

    await manager.switch_to(AppointmentStates.clinic)


window = Window(
    Jinja("make_appointment/district/header.html"),
    ScrollingGroup(
        Select(
            text=Format("{item[1].name}"),
            id=SELECT_ID,
            items="districts",
            item_id_getter=operator.itemgetter(0),
            type_factory=int,
            on_click=select_district
        ),
        id=SCROLL_ID,
        width=KB_WIDTH,
        height=KB_HEIGHT,
    ),
    get_menu_button(),
    getter=data_getter,
    state=AppointmentStates.district,
)
