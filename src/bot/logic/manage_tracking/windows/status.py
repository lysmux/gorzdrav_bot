import operator

from aiogram import F
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup,
    ListGroup,
    Url,
    Group
)
from aiogram_dialog.widgets.text import Jinja, Format, Case

from src.bot.logic.manage_tracking.states import TrackingStates
from src.bot.utils.buttons import get_back_button, get_menu_button
from src.database.models import TrackingModel
from src.gorzdrav_api import GorZdravAPI
from src.gorzdrav_api.utils import generate_gorzdrav_url, filter_appointments

KB_HEIGHT = 4
KB_WIDTH = 2

WINDOW_NAME = "tracking_status"
SCROLL_ID = f"{WINDOW_NAME}_scroll"


async def data_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
) -> dict:
    tracking: TrackingModel = (
            dialog_manager.dialog_data.get("selected_tracking") or
            dialog_manager.start_data.get("tracking")  # if from notification
    )
    appointments = await gorzdrav_api.get_appointments(
        clinic=tracking.clinic,
        doctor=tracking.doctor
    )
    filtered_appointments = filter_appointments(
        appointments=appointments,
        hours=tracking.hours
    )

    appointment_url = generate_gorzdrav_url(
        district=tracking.district,
        clinic=tracking.clinic,
        speciality=tracking.speciality,
        doctor=tracking.doctor,
    )

    return {
        "tracking": tracking,
        "filtered_appointments": (*enumerate(filtered_appointments),),
        "appointment_url": appointment_url
    }


window = Window(
    # Text
    Case(
        {
            False: Jinja("tracking/status_header.html"),
            True: Jinja("make_appointment/appointment/no_appointments.html"),
        },
        selector=F["filtered_appointments"].len() == 0
    ),

    # Appointments keyboard
    ScrollingGroup(
        ListGroup(
            Url(
                text=Format("{item[1].time_str}"),
                url=Format("{data[appointment_url]}")
            ),
            items="filtered_appointments",
            item_id_getter=operator.itemgetter(0),
        ),
        id=SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),

    # Navigation
    Group(
        get_back_button(TrackingStates.list),
        get_menu_button(),
        width=2
    ),
    getter=data_getter,
    state=TrackingStates.status
)
