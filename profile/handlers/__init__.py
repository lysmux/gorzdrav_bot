from aiogram import Router
from profile.handlers import manage_profiles, create_profile

router = Router()
router.include_routers(create_profile.router, manage_profiles.router)
