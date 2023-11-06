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

from bot.gorzdrav.dialogs.manage_tracking.states import TrackingStates
from bot.misc.buttons import MENU_BUTTON, back_button
from database.models.tracking import Tracking
from gorzdrav_api.api import GorZdravAPI
from gorzdrav_api.utils import generate_gorzdrav_url, filter_appointments

KB_HEIGHT = 4
KB_WIDTH = 2

WINDOW_NAME = "tracking_status"
LIST_SCROLL_ID = f"{WINDOW_NAME}_list_scroll"
KEYBOARD_SCROLL_ID = f"{WINDOW_NAME}_kb_scroll"
SELECT_ID = f"{WINDOW_NAME}_select"


async def status_getter(
        gorzdrav_api: GorZdravAPI,
        dialog_manager: DialogManager,
        **kwargs
):
    tracking: Tracking = (
            dialog_manager.dialog_data.get("tracking") or
            dialog_manager.start_data.get("tracking")  # if from notification
    )
    appointments = await gorzdrav_api.get_appointments(
        clinic=tracking.clinic,
        doctor=tracking.doctor
    )
    filtered_appointments = filter_appointments(
        appointments=appointments,
        time_ranges=tracking.time_ranges
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
    Case(
        {
            False: Jinja("gorzdrav/tracking/tracking/status.html"),
            True: Jinja("gorzdrav/appointment/no_appointments.html"),
        },
        selector=F["filtered_appointments"].len() == 0
    ),
    ScrollingGroup(
        ListGroup(
            Url(
                text=Format("{item[1].time_str}"),
                url=Format("{data[appointment_url]}")
            ),
            items="filtered_appointments",
            item_id_getter=operator.itemgetter(0),
        ),
        id=KEYBOARD_SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    Group(
        back_button(state=TrackingStates.list),
        MENU_BUTTON,
        width=2
    ),
    state=TrackingStates.status,
    getter=status_getter
)
