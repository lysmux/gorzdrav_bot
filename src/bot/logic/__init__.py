from . import (
    errors,
    general,
    make_appointment,
    manage_tracking,
    admin
)

routers = (
    errors.get_router(),
    general.get_router(),
    make_appointment.get_router(),
    manage_tracking.get_router(),
    admin.get_router()
)
