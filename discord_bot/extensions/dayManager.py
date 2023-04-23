from discord.ext import commands, tasks

import json, datetime


with open("./configuration.json") as json_data_file:
    raw_conf = json.load(json_data_file)

utc = datetime.timezone.utc

OPENING_CHANNEL_HOUR_TIMES = [
    datetime.time(hour=raw_conf["OPENING_CHANNEL_HOUR"], tzinfo=utc)
]

CLOSING_CHANNEL_HOUR_TIMES = [
    datetime.time(hour=raw_conf["CLOSING_CHANNEL_HOUR"], tzinfo=utc)
]

MESSAGE_HOUR_TIMES = [
    datetime.time(hour=raw_conf["FIRST_MESSAGE_HOUR"], tzinfo=utc),
    datetime.time(hour=raw_conf["SECOND_MESSAGE_HOUR"], tzinfo=utc),
    datetime.time(hour=raw_conf["THIRD_MESSAGE_HOUR"], tzinfo=utc),
]

with open("./script.json") as json_data_file:
    chatScript = json.load(json_data_file)


class DayManager(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        # ATTENTION, il recoit ses propres messages
        print("received message", message.content)



    @commands.hybrid_command(name="startbot", description="Start the bot")
    async def startBotCommand(self, ctx):
        await ctx.send("Starting the bot...")
        self.startDayJob.start()
        self.stopDayJob.start()

        self.dayNb = 1
        self.dayScript = chatScript["day" + str(self.dayNb)]["script"]
        self.messageNb = 0

        self.ctx = ctx

    # command named stopBot to stop the bot
    @commands.hybrid_command(name="stopbot", description="Stop the bot")
    async def stopBotCommand(self, ctx):
        await ctx.send("Stopping the bot...")
        self.startDayJob.stop()
        self.stopDayJob.stop()

    # Gather the messages

    # command named stopBot to stop the bot
    @commands.hybrid_command(name="nextmessage", description="Send the next message")
    async def sendMessageCommand(self, ctx):
        await self.sendMessage()

    @tasks.loop(time=OPENING_CHANNEL_HOUR_TIMES)
    async def startDayJob(self):
        self.dayNb += 1
        self.messagesJob.start()

    @tasks.loop(time=CLOSING_CHANNEL_HOUR_TIMES)
    async def stopDayJob(self):
        self.messagesJob.stop()

    @tasks.loop(time=MESSAGE_HOUR_TIMES)
    async def messagesJob(self):
        # Send messages
        await sendMessage()

    async def sendMessage(self):
        # Looping
        if self.messageNb >= len(self.dayScript):
            self.messageNb = 0

        # Get a message from the script
        await self.ctx.send(self.dayScript[self.messageNb])

        self.messageNb += 1


# Adding the cog to the bot. It is required to do this in order to use the commands
async def setup(bot) -> None:
    await bot.add_cog(DayManager(bot))
