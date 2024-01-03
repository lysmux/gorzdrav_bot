import asyncio
import logging

from aiogram import Bot
from aiogram.fsm.storage.base import BaseStorage
from aiogram_dialog import BgManagerFactory
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from src.bot.utils.template_engine import render_template
from src.config import settings
from src.database.models import TrackingModel
from src.database.repositories import TrackingRepo
from src.gorzdrav_api import GorZdravAPI
from src.gorzdrav_api.schemas import Appointment
from src.gorzdrav_api.utils import filter_appointments
from .storage import CheckerStorageProxy

logger = logging.getLogger(__name__)


class AppointmentsChecker:
    def __init__(
            self,
            db_engine: AsyncEngine,
            bot: Bot,
            storage: BaseStorage,
            manager_factory: BgManagerFactory,
    ) -> None:
        self.db_engine = db_engine
        self.bot = bot
        self.storage = storage
        self.manager_factory = manager_factory

    async def is_notified(
            self,
            tracking: TrackingModel,
            appointments: list[Appointment]
    ) -> bool:
        """
        Checks if the notification has already been sent
        """
        storage_proxy = CheckerStorageProxy(
            storage=self.storage,
            bot=self.bot,
            tracking=tracking
        )

        last_appointments = await storage_proxy.get_appointments()

        if appointments == last_appointments:
            logger.debug(f"Tracking<ID {tracking.id}> notification has already been sent")
            return True
        else:
            logger.debug(f"Tracking<ID {tracking.id}> notification sent")
            await storage_proxy.set_appointments(appointments=appointments)
            return False

    async def notify(self, tracking: TrackingModel) -> None:
        """
        Notifies user
        """
        await self.bot.send_message(
            chat_id=tracking.user.tg_id,
            text=render_template("tracking/new_appointments.html", tracking=tracking),
        )

    async def check(self, tracking: TrackingModel):
        """
        Gets appointments from API and filters its
        """
        async with GorZdravAPI() as api:
            appointments = await api.get_appointments(
                clinic=tracking.clinic,
                doctor=tracking.doctor,
            )
        filtered_appointments = filter_appointments(
            appointments=appointments,
            hours=tracking.hours
        )

        is_notified = await self.is_notified(
            tracking=tracking,
            appointments=filtered_appointments
        )

        if is_notified:
            return

        if filtered_appointments:
            await self.notify(tracking)

    async def check_all(self) -> None:
        """
        Gets all tracking from database and checks each
        """

        async with AsyncSession(bind=self.db_engine) as session:
            repository = TrackingRepo(session=session)
            all_tracking = await repository.get_all_iter(
                order_by=(TrackingModel.clinic, TrackingModel.doctor)
            )

        for tracking in all_tracking:
            await self.check(tracking)

    async def run(self) -> None:
        """
        The main loop that calls the check every `settings.check_every` minutes
        """
        while True:
            logger.info("The tracking check is started")
            await self.check_all()
            logger.info(f"The tracking check is finished. "
                        f"Repeat after {settings.check_every} minutes")

            await asyncio.sleep(settings.check_every * 60)
