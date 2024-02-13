import asyncio
import logging

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from aiogram_dialog.widgets.text.jinja import JINJA_ENV_FIELD
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.bot.setup import run_as_webhook, run_as_pooling, get_dispatcher
from src.bot.structures import TransferStruct
from src.bot.utils.set_bot_commands import set_bot_commands
from src.bot.utils.template_engine import jinja_env
from src.database import get_session_maker
from src.services import AppointmentsChecker
from src.settings import Settings

logger = logging.getLogger(__name__)


async def run_bot(settings: Settings):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    session_maker = get_session_maker(db_settings=settings.db)
    dispatcher = get_dispatcher(
        settings=settings,
        transfer_data=TransferStruct(session_maker=session_maker)
    )

    # setup bot
    bot = Bot(token=settings.bot.token, parse_mode=ParseMode.HTML)
    await set_bot_commands(bot)

    # setup aiogram dialogs
    aiod_manager_factory = setup_dialogs(dispatcher)
    setattr(bot, JINJA_ENV_FIELD, jinja_env)  # for aio dialogs

    # setup appointments checker
    appointments_checker = AppointmentsChecker(
        bot=bot,
        session_maker=session_maker,
        storage=dispatcher.storage
    )
    scheduler.add_job(
        appointments_checker.check_all,
        trigger="cron",
        hour=f"*/{settings.check_every.hour}" if settings.check_every.hour else "*",
        minute=f"*/{settings.check_every.minute}" if settings.check_every.minute else "*",
        second=f"*/{settings.check_every.second}" if settings.check_every.second else "0",
    )

    # run scheduler
    scheduler.start()

    # run bot
    if settings.use_webhook:
        await run_as_webhook(
            bot=bot,
            dispatcher=dispatcher,
            webhook_settings=settings.webhook
        )
    else:
        await run_as_pooling(
            bot=bot,
            dispatcher=dispatcher
        )


def main() -> None:
    settings = Settings()  # type: ignore

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    try:
        logger.info("GorZdrav bot is running")
        asyncio.run(run_bot(settings=settings))
    except (KeyboardInterrupt, SystemExit):
        logger.info("GorZdrav bot stopped")


if __name__ == "__main__":
    main()
