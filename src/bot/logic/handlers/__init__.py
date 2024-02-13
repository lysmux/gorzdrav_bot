from . import general, admin, make_appointment, manage_tracking

routers = (
    general.router,
    admin.router,
    make_appointment.router,
    manage_tracking.router
)
