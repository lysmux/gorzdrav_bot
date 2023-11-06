import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import (
    List,
    Format,
    Jinja,
    Const
)

from bot.gorzdrav.dialogs.appointment.states import AppointmentStates
from bot.misc.buttons import back_button
from bot.utils.aio_dialog import sync_scroll
from gorzdrav_api.api import GorZdravAPI

KB_HEIGHT = 3
KB_WIDTH = 2

WINDOW_NAME = "clinics"
LIST_SCROLL_ID = f"{WINDOW_NAME}_list_scroll"
KEYBOARD_SCROLL_ID = f"{WINDOW_NAME}_kb_scroll"
SELECT_ID = f"{WINDOW_NAME}_select"


async def clinics_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
    district = dialog_manager.dialog_data["district"]
    clinics = await gorzdrav_api.get_clinics(district=district)
    dialog_manager.dialog_data["clinics"] = clinics

    return {
        "clinics": (*enumerate(clinics),)
    }


async def clinic_handler(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int
):
    clinics = manager.dialog_data["clinics"]
    clinic = clinics[item_id]
    manager.dialog_data["clinic"] = clinic

    await manager.switch_to(AppointmentStates.speciality)


window = Window(
    Jinja("gorzdrav/appointment/clinic/header.html"),
    Const(" "),
    List(
        Jinja("gorzdrav/appointment/clinic/item.html"),
        sep="\n" * 2,
        items="clinics",
        id=LIST_SCROLL_ID,
        page_size=KB_WIDTH * KB_HEIGHT
    ),
    ScrollingGroup(
        Select(
            Format("{item[1].short_name}"),
            items="clinics",
            item_id_getter=operator.itemgetter(0),
            id=SELECT_ID,
            type_factory=int,
            on_click=clinic_handler
        ),
        id=KEYBOARD_SCROLL_ID,
        on_page_changed=sync_scroll(LIST_SCROLL_ID),
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    back_button(state=AppointmentStates.district),
    state=AppointmentStates.clinic,
    getter=clinics_getter
)
