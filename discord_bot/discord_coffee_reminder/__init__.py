import asyncio
import logging
import pytz
from datetime import datetime
from typing import List, Any

import discord
from discord import Intents

from .config import MySettings

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
        last_day_weekday = last_day.weekday()
        announce = True
        while self.running:
            await asyncio.sleep(1)
            # apply correct time zone (for docker)
            current_day = datetime.now(tz)
            logger.info(current_day)
            current_weekday = current_day.weekday()

            if current_weekday != last_day_weekday:
                # if a new day has begun a new announcement is due
                logger.info("A new day has begun...")
                announce = True

            if not self.weekday_only or current_weekday < 5:
                # only announce at weekdays..
                if announce and current_day.hour == self.reminder_hour:
                    announce = False
                    await self.call_for_coffee_break()

        logger.info("reminder thread is going down...")

    async def update_coffee_break_status(self, member, before, after):
        if after.channel and after.channel.name in self.watching_channels:
            logger.info(f"{member.display_name} joined {after.channel.name}")
            # await self.se
            if len(after.channel.members) > 1:
                await after.channel.send(
                    f"{member.display_name} initiated today's Coffee Break at {after.channel.name}")
            else:
                await after.channel.send(
                    f"{member.display_name} joined today's Coffee Break at {after.channel.name}")

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
        logger.info(f"{message.author} tried to delete message {message.content}")
        # await message.channel.send(f'Haha - {message.author} tried to delete message {message.content} - what a noob')

    async def on_voice_state_update(self, member, before, after):
        await self.update_coffee_break_status(member=member, before=before, after=after)

    async def call_for_coffee_break(self):
        logger.info("Call for Coffee Time!")
        for guild in self.guilds:
            for channel_category in guild.channels:
                if channel_category.name in self.reminder_channels:
                    await channel_category.send(f"It's {datetime.now()} - it's coffee time :)")
