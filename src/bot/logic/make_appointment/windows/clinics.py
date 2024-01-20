import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.common import sync_scroll
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import (
    List,
    Format,
    Jinja,
    Const
)

from src.bot.logic.make_appointment.states import AppointmentStates
from src.bot.utils.buttons import get_back_button
from src.gorzdrav_api import GorZdravAPI

KB_HEIGHT = 3
KB_WIDTH = 2

WINDOW_NAME = "clinics"
LIST_ID = f"{WINDOW_NAME}_list"
SCROLL_ID = f"{WINDOW_NAME}_scroll"
SELECT_ID = f"{WINDOW_NAME}_select"


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
    """
    Get clinics from API
    """
    district = dialog_manager.dialog_data["district"]
    clinics = await gorzdrav_api.get_clinics(district=district)
    dialog_manager.dialog_data["clinics"] = clinics

    return {
        "clinics": (*enumerate(clinics),)
    }


async def select_clinic(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: int
) -> None:
    """
    Switch to the speciality selection
    """

    clinics = manager.dialog_data["clinics"]
    clinic = clinics[item_id]
    manager.dialog_data["clinic"] = clinic

    await manager.switch_to(AppointmentStates.speciality)


window = Window(
    Jinja("make_appointment/clinic/header.html"),
    Const(" "),
    List(
        Jinja("make_appointment/clinic/item.html"),
        sep="\n" * 2,
        items="clinics",
        id=LIST_ID,
        page_size=KB_WIDTH * KB_HEIGHT
    ),
    ScrollingGroup(
        Select(
            Format("{item[1].short_name}"),
            items="clinics",
            item_id_getter=operator.itemgetter(0),
            id=SELECT_ID,
            type_factory=int,
            on_click=select_clinic
        ),
        id=SCROLL_ID,
        on_page_changed=sync_scroll(LIST_ID),
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    get_back_button(AppointmentStates.district),
    getter=data_getter,
    state=AppointmentStates.clinic
)
