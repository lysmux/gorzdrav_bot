from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Jinja, Const

from bot import keyboard_texts
from bot.logic.manage_tracking.states import TrackingStates
from .states import NewAppointmentsStates

SEE_APPOINTMENTS_BTN_ID = "see_appointments_btn"


async def tracking_status(
        callback: CallbackQuery,
        widget: Button,
        manager: DialogManager,
) -> None:
    await manager.start(
        state=TrackingStates.status,
        data={
            "tracking": manager.start_data["tracking"],
        }
    )


window = Window(
    Jinja("new_appointments/header.html"),
    Button(
        Const(keyboard_texts.new_appointments.SEE_APPOINTMENTS),
        id=SEE_APPOINTMENTS_BTN_ID,
        on_click=tracking_status
    ),
    state=NewAppointmentsStates.notify
)
