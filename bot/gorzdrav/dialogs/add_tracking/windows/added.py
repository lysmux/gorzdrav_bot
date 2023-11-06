from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group
from aiogram_dialog.widgets.text import Jinja

from bot.gorzdrav.dialogs.add_tracking.states import AddTrackingStates
from bot.misc.buttons import MENU_BUTTON, back_button

window = Window(
    Jinja("gorzdrav/tracking/tracking/added.html"),
    Group(
        back_button(state=AddTrackingStates.add),
        MENU_BUTTON,
        width=2
    ),
    state=AddTrackingStates.added,
)
