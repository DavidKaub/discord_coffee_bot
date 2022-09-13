import asyncio
import logging
import pytz
from datetime import datetime
from typing import List, Any

import discord
from discord import Intents

from .config import MySettings
from .util import get_random_tenor_gif

app_settings = MySettings()

logging.basicConfig(level=app_settings.LOGGING_LEVEL)
logger = logging.getLogger(__name__)


class MyClient(discord.Client):

    def __init__(self, *, intents: Intents, reminder_hour: int, reminder_channels: List[str],
                 watching_channels: List[str], weekday_only: bool, **options: Any):

        super().__init__(intents=intents, **options)
        self.reminder_hour = reminder_hour
        self.started: bool = False
        self.running: bool = True
        self.reminder_channels: List[str] = reminder_channels
        self.watching_channels: List[str] = watching_channels
        self.weekday_only = weekday_only

    async def run_reminder(self) -> None:
        logger.info("Starting reminder thread...")
        tz = pytz.timezone(app_settings.TIME_ZONE)
        last_day = datetime.now(tz)
        logger.info(last_day)
        last_day_weekday = last_day.weekday()
        announce = True
        while self.running:
            await asyncio.sleep(5)
            # apply correct time zone (for docker)
            current_day = datetime.now(tz)
            current_weekday = current_day.weekday()

            if current_weekday != last_day_weekday:
                # if a new day has begun a new announcement is due
                logger.info(f"A new day has begun {current_day}")
                announce = True

            if not self.weekday_only or current_weekday < 5:
                # only announce at weekdays..
                if announce and current_day.hour == self.reminder_hour:
                    announce = False
                    await self.call_for_coffee_break(current_day)

        logger.info("reminder thread is going down...")

    async def update_coffee_break_status(self, member, before, after):
        if after.channel and after.channel.name in self.watching_channels:
            logger.info(f"{member.display_name} joined {after.channel.name}")
            # await self.se
            if len(after.channel.members) <= 1:
                await self.send_message_to_reminder_channels(
                    f"{member.display_name} initiated session at {after.channel.name}")

    async def on_ready(self):
        if not self.started:
            asyncio.get_event_loop().create_task(self.run_reminder())

        logger.info(f'Logged on as {self.user}!')

    async def on_message(self, message):
        logger.info(f'Message from {message.author}: {message.content}')

    async def on_voice_server_update(self, data):
        logger.info('Voice from')
        logger.info(data)

    async def on_message_delete(self, message):
        pass
        # logger.info(f"{message.author} tried to delete message {message.content}")
        # await message.channel.send(f'Haha - {message.author} tried to delete message {message.content} - what a noob')

    async def on_voice_state_update(self, member, before, after):
        logger.info("Voice status update...")
        await self.update_coffee_break_status(member=member, before=before, after=after)

    async def call_for_coffee_break(self, current_date: datetime):
        logger.info("Call for Coffee Time!")
        day_as_string = current_date.strftime("%Y-%m-%d")
        time_as_string = current_date.strftime("%H:%M")
        await self.send_message_to_reminder_channels(f"It's the {day_as_string} at {time_as_string} o'clock  - it's "
                                                     f"coffee time :)")
        await self.send_message_to_reminder_channels(get_random_tenor_gif(app_settings.TENOR_SEARCH_TOPIC))

    async def send_message_to_reminder_channels(self, message):
        logger.info(f"Bot sending message: {message}")
        for guild in self.guilds:
            for channel_category in guild.channels:
                if channel_category.name in self.reminder_channels:
                    await channel_category.send(message)
