from . import (
    appointment,
    add_tracking,
    manage_tracking,
    new_appointment
)

routers = (
    appointment.dialog,
    add_tracking.dialog,
    manage_tracking.dialog,
    new_appointment.dialog
)
