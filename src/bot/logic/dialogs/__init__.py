from . import general, admin, make_appointment, manage_tracking

routers = (
    general.dialog,
    admin.dialog,
    make_appointment.dialog,
    manage_tracking.dialog
)
