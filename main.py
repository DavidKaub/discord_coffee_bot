import logging

import discord
from discord_coffee_reminder import MyClient
from discord_coffee_reminder.config import MySettings

app_settings = MySettings()

logging.basicConfig(level=app_settings.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # intents = discord.Intents.default()
    # intents.message_content = True
    intents = discord.Intents(messages=True, guilds=True)
    client = MyClient(intents=intents, reminder_hour=app_settings.DISCORD_REMINDER_HOUR,
                      reminder_channels=app_settings.reminder_channels,
                      watching_channels=app_settings.watching_channels,
                      week_day_only=app_settings.WEEKDAY_ONLY)
    client.run(app_settings.DISCORD_BOT_TOKEN)
    # stop reminder if bot is not running...
    client.running = False
