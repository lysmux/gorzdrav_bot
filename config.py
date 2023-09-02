import configparser
from dataclasses import dataclass


@dataclass
class Database:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class Bot:
    token: str
    use_redis: bool


@dataclass
class Config:
    bot: Bot
    db: Database

    @classmethod
    def load_config(cls, path: str):
        config = configparser.ConfigParser()
        config.read(path)

        bot_config = config["bot"]
        db_config = config["database"]

        return cls(
            bot=Bot(
                token=bot_config.get("token"),
                use_redis=bot_config.getboolean("use_redis"),
            ),
            db=Database(
                host=db_config.get("host"),
                port=db_config.getint("port"),
                user=db_config.get("user"),
                password=db_config.get("password"),
                database=db_config.get("database")
            ),
        )
