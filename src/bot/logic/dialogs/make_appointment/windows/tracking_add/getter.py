from enum import auto, StrEnum
from typing import Any

from src.bot.multimedia import keyboard_texts


class TimeRangeEnum(StrEnum):
    ALL_DAY = auto()
    MORNING = auto()
    AFTERNOON = auto()
    EVENING = auto()


async def data_getter(**kwargs) -> dict[str, Any]:
    return {
        "ranges": (
            (keyboard_texts.tracking.MORNING, TimeRangeEnum.MORNING),
            (keyboard_texts.tracking.AFTERNOON, TimeRangeEnum.AFTERNOON),
            (keyboard_texts.tracking.EVENING, TimeRangeEnum.EVENING),
            (keyboard_texts.tracking.ALL_DAY, TimeRangeEnum.ALL_DAY),
        )
    }
