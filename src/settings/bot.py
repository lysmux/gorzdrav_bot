from pydantic import BaseModel


class BotSettings(BaseModel):
    token: str
