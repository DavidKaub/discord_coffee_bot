import threading
import time
from datetime import datetime
from pydantic import BaseSettings
import discord


class MySettings(BaseSettings):
    discord_bot_token: str


app_settings = MySettings()


class Remainder(threading.Thread):
    running = True

    def __init__(self, discord_client):
        print("init")
        # calling parent class constructor
        threading.Thread.__init__(self)
        self.discord_client = discord_client

    def run(self) -> None:
        print("Star reminder thread...")
        last_day = datetime.today()
        last_day_weekday = last_day.weekday()
        announce = True
        while self.running:
            current_day = datetime.today()
            current_weekday = current_day.weekday()

            if current_weekday != last_day_weekday:
                # if a new day has begun a new announcement is due
                print("A new day has begun...")
                announce = True

            if current_weekday < 5:
                # only announce at weekdays..
                if announce and current_day.hour == 10:
                    # announcement is due at 10 -> minutes don't matter as long is only executed once
                    # therefore no longer required: and current_day.minute == 00:
                    print("yeah...")
                    # todo announce using discord._client
                    announce = False

            time.sleep(59)

        print("reminder thread is going down...")


async def update_coffee_break_status(member, before, after):
    if after.channel and after.channel.name == "Gaming":
        print(f"{member.display_name} joined {after.channel.name}")
        # await self.se
        if len(after.channel.members) > 1:
            await after.channel.send(
                f"{member.display_name} initiated today's Coffee Break at {after.channel.name}")
        else:
            await after.channel.send(f"{member.display_name} joined today's Coffee Break at {after.channel.name}")


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

    async def on_voice_server_update(self, data):
        print('Voice from')
        print(data)

    async def on_message_delete(self, message):
        pass
        print(f"{message.author} tried to delete message {message.content}")
        # await message.channel.send(f'Haha - {message.author} tried to delete message {message.content} - what a noob')

    async def on_voice_state_update(self, member, before, after):
        await update_coffee_break_status(member=member, before=before, after=after)

    async def call_for_coffee_break(self):
        print("Coffee Time!")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
reminder = Remainder(discord_client=client)
reminder.start()
client.run(app_settings.discord_bot_token)
# stop reminder if coffee break is not running...
reminder.running = False
