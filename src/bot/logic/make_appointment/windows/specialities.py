import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Jinja

from bot.utils.buttons import get_back_button
from gorzdrav_api import GorZdravAPI
from ..states import AppointmentStates

KB_HEIGHT = 4
KB_WIDTH = 1

WINDOW_NAME = "specialities"
SCROLL_ID = f"{WINDOW_NAME}_scroll"
SELECT_ID = f"{WINDOW_NAME}_select"


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
    """
    Get specialities from API
    """

    clinic = dialog_manager.dialog_data["clinic"]
    specialities = await gorzdrav_api.get_specialities(clinic=clinic)
    dialog_manager.dialog_data["specialities"] = specialities

    return {
        "specialities": (*enumerate(specialities),)
    }


async def select_speciality(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int
):
    """
    Switch to the doctor selection
    """

    specialities = manager.dialog_data["specialities"]
    speciality = specialities[item_id]
    manager.dialog_data["speciality"] = speciality

    await manager.switch_to(AppointmentStates.doctor)


window = Window(
    Jinja("make_appointment/speciality/header.html"),
    ScrollingGroup(
        Select(
            Format("{item[1].name}"),
            items="specialities",
            item_id_getter=operator.itemgetter(0),
            id=SELECT_ID,
            type_factory=int,
            on_click=select_speciality
        ),
        id=SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    get_back_button(),
    getter=data_getter,
    state=AppointmentStates.speciality
)
