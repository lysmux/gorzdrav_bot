from aiogram import Router
from bot.profile.handlers import manage_profiles, create_profile

router = Router()
router.include_routers(create_profile.router, manage_profiles.router)
