import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import (
    Format,
    Const,
    List,
    Jinja
)

from src.bot.logic.gorzdrav.dialogs.appointment.states import AppointmentStates
from src.bot.misc.buttons import back_button
from src.bot.utils.aio_dialog import sync_scroll
from src.gorzdrav_api.api import GorZdravAPI

KB_HEIGHT = 3
KB_WIDTH = 2

WINDOW_NAME = "doctors"
LIST_SCROLL_ID = f"{WINDOW_NAME}_list_scroll"
KEYBOARD_SCROLL_ID = f"{WINDOW_NAME}_kb_scroll"
SELECT_ID = f"{WINDOW_NAME}_select"


async def doctors_window_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
    speciality = dialog_manager.dialog_data["speciality"]
    clinic = dialog_manager.dialog_data["clinic"]
    doctors = await gorzdrav_api.get_doctors(clinic=clinic, speciality=speciality)
    dialog_manager.dialog_data["doctors"] = doctors

    return {
        "doctors": (*enumerate(doctors),)
    }


async def doctor_handler(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int
):
    doctors = manager.dialog_data["doctors"]
    doctor = doctors[item_id]
    manager.dialog_data["doctor"] = doctor

    await manager.switch_to(AppointmentStates.appointment)


window = Window(
    Jinja("gorzdrav/appointment/doctor/header.html"),
    Const(" "),
    List(
        Jinja("gorzdrav/appointment/doctor/item.html"),
        sep="\n" * 2,
        items="doctors",
        id=LIST_SCROLL_ID,
        page_size=KB_WIDTH * KB_HEIGHT
    ),
    ScrollingGroup(
        Select(
            Format("{item[1].short_name}"),
            items="doctors",
            item_id_getter=operator.itemgetter(0),
            id=SELECT_ID,
            type_factory=int,
            on_click=doctor_handler
        ),
        id=KEYBOARD_SCROLL_ID,
        on_page_changed=sync_scroll(LIST_SCROLL_ID),
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    back_button(state=AppointmentStates.speciality),
    state=AppointmentStates.doctor,
    getter=doctors_window_getter
)
