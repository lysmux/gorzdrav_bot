import datetime

months = ("января", "февраля", "марта", "апреля", "мая", "июня", "июля",
          "августа", "сентября", "октября", "ноября", "декабря")


def datetime_to_str(dt: datetime.datetime) -> str:
    day = dt.day
    month = months[dt.month - 1]
    time = dt.strftime("%H:%M")

    return f"{day} {month} в {time}"
