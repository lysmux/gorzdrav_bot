import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Jinja

from src.bot.logic.gorzdrav.dialogs.appointment.states import AppointmentStates
from src.bot.misc.buttons import back_button
from src.gorzdrav_api.api import GorZdravAPI

KB_HEIGHT = 4
KB_WIDTH = 1

WINDOW_NAME = "specialities"
KEYBOARD_SCROLL_ID = f"{WINDOW_NAME}_kb_scroll"
SELECT_ID = f"{WINDOW_NAME}_select"


async def specialities_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
    clinic = dialog_manager.dialog_data["clinic"]
    specialities = await gorzdrav_api.get_specialities(clinic=clinic)
    dialog_manager.dialog_data["specialities"] = specialities

    return {
        "specialities": (*enumerate(specialities),)
    }


async def speciality_handler(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int
):
    specialities = manager.dialog_data["specialities"]
    speciality = specialities[item_id]
    manager.dialog_data["speciality"] = speciality

    await manager.switch_to(AppointmentStates.doctor)


window = Window(
    Jinja("gorzdrav/appointment/speciality/header.html"),
    ScrollingGroup(
        Select(
            Format("{item[1].name}"),
            items="specialities",
            item_id_getter=operator.itemgetter(0),
            id=SELECT_ID,
            type_factory=int,
            on_click=speciality_handler
        ),
        id=KEYBOARD_SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    back_button(state=AppointmentStates.clinic),
    state=AppointmentStates.speciality,
    getter=specialities_getter
)
