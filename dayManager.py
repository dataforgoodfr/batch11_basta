import aiocron
import asyncio

from discord.ext import commands, tasks


class DayManager:
    def __init__(self, configuration, bot, chatScript):
        self.bot = bot
        self.chatScript = chatScript

        # We need something like `@aiocron.crontab(someCronConfiguration, start=False)` before each job
        # but because we cannot put variable inside of decorator, we will need to declare them inside our init func
        # like in the last exemple in [this](https://pypi.org/project/aiocron/) page
        self.setJobsConfiguration(configuration)

        # We cannot use bot.hybrid_command because the bot is not yet defined so we use the other form and then add them to the bot in the setJobsConfiguration function
        self.load_commands()

    def load_commands(self):
        @self.bot.hybrid_command(name="startbot", description="Start the bot")
        async def startBotCommand(ctx):
            await ctx.send("Starting the bot...")
            self.startDayJob.start()
            self.stopDayJob.start()

            self.dayNb = 1
            print(self.chatScript)
            self.dayScript = self.chatScript["day" + str(self.dayNb)]["script"]
            print(self.dayScript)
            self.messageNb = 0

            self.ctx = ctx

        # command named stopBot to stop the bot
        @self.bot.hybrid_command(name="stopbot", description="Stop the bot")
        async def stopBotCommand(ctx):
            await ctx.send("Stopping the bot...")
            self.startDayJob.stop()
            self.stopDayJob.stop()

        # Gather the messages

        # command named stopBot to stop the bot
        @self.bot.hybrid_command(
            name="nextmessage", description="Send the next message"
        )
        async def sendMessageCommand(ctx):
            await self.sendMessage()

    async def startDayJob(self):
        self.dayNb += 1
        self.messagesJob.start()

    async def stopDayJob(self):
        self.messagesJob.stop()

    async def messagesJob(self):
        # Send messages
        await sendMessage()

    @tasks.loop(seconds=5.0)
    async def sendMessage(self):
        # Looping
        if self.messageNb >= len(self.dayScript):
            self.messageNb = 0

        # Get a message from the script
        await self.ctx.send(self.dayScript[self.messageNb])

        self.messageNb += 1

    def setJobsConfiguration(self, conf):
        self.startDayJob = aiocron.crontab(
            conf["OPENING_CHANNEL_HOUR_CRON"], func=self.startDayJob, start=False
        )

        self.stopDayJob = aiocron.crontab(
            conf["CLOSING_CHANNEL_HOUR_CRON"], func=self.stopDayJob, start=False
        )

        self.messagesJob = aiocron.crontab(
            # conf["MESSAGE_CRON"], func=self.messagesJob, start=False
            "* * * * * *",
            func=self.messagesJob,
            start=False,
        )
