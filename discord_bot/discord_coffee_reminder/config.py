import logging
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class MySettings(BaseSettings):
    LOGGING_LEVEL = logging.INFO
    TIME_ZONE: str = "Europe/Berlin"
    DISCORD_BOT_TOKEN: str
    DISCORD_REMINDER_HOUR: int = 18
    WEEKDAY_ONLY: bool = True
    reminder_channels: List[str] = ["Gaming", "Coffee break", "announcements", "bot_announcements"]
    watching_channels: List[str] = ["Gaming", "Coffee break"]
