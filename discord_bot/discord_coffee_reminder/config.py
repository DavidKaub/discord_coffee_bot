import logging
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class MySettings(BaseSettings):
    LOGGING_LEVEL = logging.INFO
    TIME_ZONE: str = "Europe/Berlin"
    DISCORD_BOT_TOKEN: str
    DISCORD_REMINDER_HOUR: int = 10
    WEEKDAY_ONLY: bool = True
    reminder_channels: List[str] = ["announcements", "bot_announcements"]
    watching_channels: List[str] = ["Gaming", "Coffee break"]
    TENOR_API_KEY = "LIVDSRZULELA"  # default test value from tenor api doc
    TENOR_SEARCH = True
    TENOR_SEARCH_TOPIC = "coffee"
