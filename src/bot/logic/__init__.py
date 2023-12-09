from . import (
    errors,
    general,
    make_appointment,
    manage_tracking,
    new_appointments
)

routers = (
    errors.get_router(),
    general.get_router(),
    make_appointment.get_router(),
    manage_tracking.get_router(),
    new_appointments.get_router()
)
