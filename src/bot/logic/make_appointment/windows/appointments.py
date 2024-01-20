import operator

from aiogram import F
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup,
    ListGroup,
    Url,
    Group,
    SwitchTo
)
from aiogram_dialog.widgets.text import (
    Format,
    Jinja,
    Case,
    Const
)

from src.bot.logic.make_appointment.states import AppointmentStates
from src.bot.multimedia import keyboard_texts
from src.bot.utils.buttons import get_menu_button, get_back_button
from src.gorzdrav_api import GorZdravAPI
from src.gorzdrav_api.utils import generate_gorzdrav_url

KB_HEIGHT = 4
KB_WIDTH = 2

WINDOW_NAME = "appointments"
SCROLL_ID = f"{WINDOW_NAME}_scroll"
LIST_ID = f"{WINDOW_NAME}_list"
ADD_TRACKING_BTN_ID = f"{WINDOW_NAME}_add_tracking_btn"


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
    """
    Get appointments from API
    """

    district = dialog_manager.dialog_data["district"]
    clinic = dialog_manager.dialog_data["clinic"]
    speciality = dialog_manager.dialog_data["speciality"]
    doctor = dialog_manager.dialog_data["doctor"]

    appointments = await gorzdrav_api.get_appointments(clinic=clinic, doctor=doctor)
    appointment_url = generate_gorzdrav_url(
        district=district,
        clinic=clinic,
        speciality=speciality,
        doctor=doctor,
    )

    return {
        "appointments": (*enumerate(appointments),),
        "appointment_url": appointment_url
    }


window = Window(
    Case(
        {
            False: Jinja("make_appointment/appointment/header.html"),
            True: Jinja("make_appointment/appointment/no_appointments.html"),
        },
        selector=F["appointments"].len() == 0
    ),
    ScrollingGroup(
        ListGroup(
            Url(
                text=Format("{item[1].time_str}"),
                url=Format("{data[appointment_url]}")
            ),
            items="appointments",
            item_id_getter=operator.itemgetter(0),
            id=LIST_ID
        ),
        id=SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    SwitchTo(
        Const(keyboard_texts.make_appointment.ADD_TRACKING),
        id=ADD_TRACKING_BTN_ID,
        state=AppointmentStates.tracking_add
    ),
    Group(
        get_back_button(AppointmentStates.doctor),
        get_menu_button(),
        width=2
    ),
    getter=data_getter,
    state=AppointmentStates.appointment
)
