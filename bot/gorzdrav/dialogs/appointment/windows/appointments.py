import operator

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup,
    ListGroup,
    Url,
    Group,
    Button
)
from aiogram_dialog.widgets.text import (
    Const,
    Format,
    Jinja,
    Case
)

from bot.gorzdrav.dialogs.add_tracking.states import AddTrackingStates
from bot.gorzdrav.dialogs.appointment.button_texts import ADD_TRACKING
from bot.gorzdrav.dialogs.appointment.states import AppointmentStates
from bot.misc.buttons import MENU_BUTTON, back_button
from gorzdrav_api.api import GorZdravAPI
from gorzdrav_api.utils import generate_gorzdrav_url

KB_HEIGHT = 4
KB_WIDTH = 2

WINDOW_NAME = "appointments"
LIST_SCROLL_ID = f"{WINDOW_NAME}_list_scroll"
KEYBOARD_SCROLL_ID = f"{WINDOW_NAME}_kb_scroll"
SELECT_ID = f"{WINDOW_NAME}_select"

ADD_TRACKING_BTN_ID = "add_tracking_btn"


async def appointments_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
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


async def go_add_tracking(
        callback: CallbackQuery,
        widget: Button,
        manager: DialogManager,
):
    await manager.start(
        state=AddTrackingStates.add,
        data={
            "district": manager.dialog_data["district"],
            "clinic": manager.dialog_data["clinic"],
            "speciality": manager.dialog_data["speciality"],
            "doctor": manager.dialog_data["doctor"],
        }
    )


window = Window(
    Case(
        {
            False: Jinja("gorzdrav/appointment/appointment/header.html"),
            True: Jinja("gorzdrav/appointment/appointment/no_appointments.html"),
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
        ),
        id=KEYBOARD_SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    Button(
        Const(ADD_TRACKING),
        id=ADD_TRACKING_BTN_ID,
        on_click=go_add_tracking
    ),
    Group(
        back_button(state=AppointmentStates.doctor),
        MENU_BUTTON,
        width=2
    ),
    state=AppointmentStates.appointment,
    getter=appointments_getter
)
