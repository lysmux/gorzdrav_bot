from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Jinja, Const

from bot.gorzdrav.dialogs.manage_tracking.states import TrackingStates
from bot.gorzdrav.dialogs.new_appointment.button_texts import SEE_APPOINTMENTS
from bot.gorzdrav.dialogs.new_appointment.states import NewAppointmentStates

SEE_APPOINTMENT_BTN_ID = "see_appointment_btn"


async def go_tracking_status(
        callback: CallbackQuery,
        widget: Button,
        manager: DialogManager,
):
    await manager.start(
        state=TrackingStates.status,
        data={
            "tracking": manager.start_data["tracking"],
        }
    )


window = Window(
    Jinja("gorzdrav/tracking/new_appointment.html"),
    Button(
        Const(SEE_APPOINTMENTS),
        id=SEE_APPOINTMENT_BTN_ID,
        on_click=go_tracking_status
    ),
    state=NewAppointmentStates.notify
)
