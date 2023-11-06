import asyncio
import logging
from itertools import groupby

from aiogram import Bot
from aiogram.fsm.storage.base import StorageKey, BaseStorage
from aiogram_dialog import BgManagerFactory, StartMode
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.gorzdrav.dialogs.new_appointment.states import NewAppointmentStates
from database.database import Repository
from database.models.tracking import Tracking
from gorzdrav_api.api import GorZdravAPI
from gorzdrav_api.exceptions import GorZdravError
from gorzdrav_api.schemas import Appointment
from gorzdrav_api.utils import filter_appointments

logger = logging.getLogger("appointments checker")


class AppointmentsChecker:
    def __init__(
            self,
            bot: Bot,
            manager_factory: BgManagerFactory,
            storage: BaseStorage,
            database_pool: async_sessionmaker,
            check_every: int,
    ):
        self.bot = bot
        self.manager_factory = manager_factory
        self.storage = storage
        self.database_pool = database_pool
        self.check_every = check_every

    async def is_notified(
            self,
            tracking: Tracking,
            appointments: list[Appointment]
    ):
        key = StorageKey(
            bot_id=self.bot.id,
            chat_id=tracking.tg_user_id,
            user_id=tracking.tg_user_id,
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

    async def check(self):
        logger.debug("Search for appointments started")

        async with self.database_pool() as session:
            repository = Repository(session)
            all_tracking = await repository.get_all_tracking()

        grouped_tracking = groupby(all_tracking, key=lambda x: (x.clinic, x.doctor))
        for key, group in grouped_tracking:
            clinic, doctor = key
            async with GorZdravAPI() as api:
                try:
                    appointments = await api.get_appointments(
                        clinic=clinic,
                        doctor=doctor
                    )
                except GorZdravError:
                    continue

            for tracking in group:
                filtered_appointments = filter_appointments(
                    appointments=appointments,
                    time_ranges=tracking.time_ranges
                )

                if filtered_appointments:
                    await self.notify(
                        tracking=tracking,
                        appointments=filtered_appointments
                    )

        logger.debug(f"Search for appointments ended. Repeat after {self.check_every} minutes")

    async def notify(
            self,
            tracking: Tracking,
            appointments: list[Appointment]
    ):
        if await self.is_notified(tracking, appointments):
            logger.debug(f"Tracking (ID {tracking.id}) notification has already been sent")
            return

        manager = self.manager_factory.bg(
            bot=self.bot,
            user_id=tracking.tg_user_id,
            chat_id=tracking.tg_user_id
        )
        await manager.start(
            NewAppointmentStates.notify,
            data={"tracking": tracking},
            mode=StartMode.NEW_STACK
        )

        logger.debug(f"Tracking (ID {tracking.id}) notification sent")

    async def run(self):
        while True:
            await self.check()
            await asyncio.sleep(self.check_every * 60)
