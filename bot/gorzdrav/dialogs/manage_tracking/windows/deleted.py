from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group
from aiogram_dialog.widgets.text import Jinja

from bot.misc.buttons import MENU_BUTTON, back_button
from bot.gorzdrav.dialogs.manage_tracking.states import TrackingStates

window = Window(
    Jinja("gorzdrav/tracking/tracking/deleted.html"),
    Group(
        back_button(state=TrackingStates.list),
        MENU_BUTTON,
        width=2
    ),
    state=TrackingStates.deleted,
)
