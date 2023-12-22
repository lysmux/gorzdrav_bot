import asyncio
import logging
from itertools import groupby

from aiogram import Bot
from aiogram.fsm.storage.base import StorageKey, BaseStorage
from aiogram_dialog import BgManagerFactory, StartMode
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.bot.logic.new_appointments.states import NewAppointmentsStates
from src.database.models import TrackingModel
from src.database.repositories import TrackingRepo
from src.gorzdrav_api import GorZdravAPI
from src.gorzdrav_api.exceptions import GorZdravError
from src.gorzdrav_api.schemas import Appointment
from src.gorzdrav_api.utils import filter_appointments

logger = logging.getLogger("Appointments checker")


class AppointmentsChecker:
    def __init__(
            self,
            bot: Bot,
            manager_factory: BgManagerFactory,
            storage: BaseStorage,
            db_engine: AsyncEngine,
            check_every: int,
    ):
        self.bot = bot
        self.manager_factory = manager_factory
        self.storage = storage
        self.db_engine = db_engine
        self.check_every = check_every

    async def is_notified(
            self,
            tracking: TrackingModel,
            appointments: list[Appointment]
    ) -> bool:
        key = StorageKey(
            bot_id=self.bot.id,
            chat_id=tracking.user.tg_id,
            user_id=tracking.user.tg_id,
            destiny=f"checker:{tracking.id}"
        )
        data = await self.storage.get_data(key)
        last_appointments = data.get("last_appointments")

        if last_appointments == appointments:
            return True

        await self.storage.set_data(
            key=key,
            data={"last_appointments": appointments}
        )
        return False

    async def notify(self, tracking: TrackingModel):

        manager = self.manager_factory.bg(
            bot=self.bot,
            user_id=tracking.user.tg_id,
            chat_id=tracking.user.tg_id
        )
        await manager.start(
            NewAppointmentsStates.notify,
            data={"tracking": tracking},
            mode=StartMode.NEW_STACK
        )

        logger.debug(f"Tracking (ID {tracking.id}) notification sent")

    async def check(self):
        logger.debug("Search for appointments started")

        async with AsyncSession(self.db_engine) as session:
            repository = TrackingRepo(session)
            all_tracking = await repository.get_all_iter()

        grouped_tracking = groupby(all_tracking, key=lambda x: (x.clinic, x.doctor))
        for key, group in grouped_tracking:
            clinic, doctor = key
            async with GorZdravAPI() as api:
                try:
                    appointments = await api.get_appointments(
                        clinic=clinic,
                        doctor=doctor
                    )
                except GorZdravError:  # todo optimize this
                    continue

            for tracking in group:
                filtered_appointments = filter_appointments(
                    appointments=appointments,
                    time_ranges=tracking.time_ranges
                )

                if await self.is_notified(tracking, appointments):
                    logger.debug(f"Tracking (ID {tracking.id}) notification has already been sent")
                    continue

                if filtered_appointments:
                    await self.notify(tracking=tracking)

        logger.debug(f"Search for appointments ended. "
                     f"Repeat after {self.check_every} minutes")

    async def run(self):
        while True:
            await self.check()
            await asyncio.sleep(self.check_every * 60)
