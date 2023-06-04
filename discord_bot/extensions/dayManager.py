from dataclasses import dataclass
from datetime import time, timezone
from json import load

from discord.ext import commands, tasks

__all__ = ["DayManager"]

with open("./configuration.json") as json_data_file:
    raw_conf = load(json_data_file)

utc = timezone.utc

OPENING_CHANNEL_HOUR_TIMES = [
    time(hour=raw_conf["OPENING_CHANNEL_HOUR"], tzinfo=utc)
]

CLOSING_CHANNEL_HOUR_TIMES = [
    time(hour=raw_conf["CLOSING_CHANNEL_HOUR"], tzinfo=utc)
]

MESSAGE_HOUR_TIMES = [
    time(hour=raw_conf["FIRST_MESSAGE_HOUR"], tzinfo=utc),
    time(hour=raw_conf["SECOND_MESSAGE_HOUR"], tzinfo=utc),
    time(hour=raw_conf["THIRD_MESSAGE_HOUR"], tzinfo=utc),
]

with open("./script.json") as json_data_file:
    chat_script = load(json_data_file)


@dataclass
class DayManager(commands.Cog):
    bot: commands.Bot

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        # ATTENTION, il recoit ses propres messages
        print("received message", message.content)

    @commands.hybrid_command(name="startbot", description="Start the bot")
    async def start_bot_command(self, ctx):
        await ctx.send("Starting the bot...")
        self.start_day_job.start()
        self.stop_day_job.start()

        self.day_nb = 1
        self.day_script = chat_script["day" + str(self.day_nb)]["script"]
        self.message_nb = 0

        self.ctx = ctx

    # command named stopBot to stop the bot
    @commands.hybrid_command(name="stopbot", description="Stop the bot")
    async def stopBotCommand(self, ctx):
        await ctx.send("Stopping the bot...")
        self.start_day_job.stop()
        self.stop_day_job.stop()

    # Gather the messages

    # command named stopBot to stop the bot
    @commands.hybrid_command(
        name="nextmessage", description="Send the next message"
    )
    async def sendMessageCommand(self, ctx):
        await self.sendMessage()

    @tasks.loop(time=OPENING_CHANNEL_HOUR_TIMES)
    async def start_day_job(self):
        self.day_nb += 1
        self.messages_job.start()

    @tasks.loop(time=CLOSING_CHANNEL_HOUR_TIMES)
    async def stop_day_job(self):
        self.messages_job.stop()

    @tasks.loop(time=MESSAGE_HOUR_TIMES)
    async def messages_job(self):
        # Send messages
        await self.sendMessage()

    async def sendMessage(self):
        # Looping
        if self.message_nb >= len(self.day_script):
            self.message_nb = 0

        # Get a message from the script
        await self.ctx.send(self.day_script[self.message_nb])

        self.message_nb += 1


# Adding the cog to the bot
# It is required to do this in order to use the commands
async def setup(bot) -> None:
    await bot.add_cog(DayManager(bot))
