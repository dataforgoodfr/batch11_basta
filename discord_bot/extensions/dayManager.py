import typing
from dataclasses import dataclass

import helpers.constantsImport as dataImport
from discord.ext import commands, tasks

__all__ = ["DayManager"]


@dataclass
class DayManager(commands.Cog):
    bot: commands.Bot

    def __post_init__(self):
        self.tools = self.bot.get_cog("Tools")

    """
    This class is used to manage the bot behaviour during the days.
    The bot is supposed to be started with the `startbot` command.
    However, is makes no sense the bot starting command is in this file.
    TODO : Make a starting command in the bot.py (main file) that will then use this function

    It is supposed to be stopped with the appropriate stopbot command.

    The bot configuration is stored in the configuration.json file.

    The script is stored in the script.json file. This file should be left where it is because it is part of the main bot configuration.


    Attributes
    ----------
    Takes the bot as an argument in order to be able to add it to the cog.

    Methods
    ----------
        Commands :
            start_bot_command : starts the bot. Please add the appropriate parameters in order to generate daily conclusions (at the end of the day) and a final conclusion
            stop_bot_command : stops the bot. Please add the appropriate parameters in order to generate daily conclusions (at the end of the day) and a final conclusion
            send_message_command : Force the sending of the next message (using the send_message function)
            start_day : Force the start of the day (using the start_day_job task function)
            stop_day : Force the stop of the day (using the stop_day_job task function)

        Taks (repetitive functions):
            start_day_job  : Coroutine to start the day at a given time (in the configuration file). Also starts the messages_job coroutine
            stop_day_job : Coroutine to stop the day at a given time (in the configuration file). Also stops the messages_job coroutine
            after_stop_day_job : Occurs after the execution of the stop_day_job coroutine.
                If is was the final day and the appropriate flag was set, it will generate the final conclusion, else if the appropriate flag was set, it will generate the daily conclusion
            messages_job : Coroutine to send the messages at the appropriate time (in the configuration file). Started and stopped by the start_day_job and stop_day_job coroutines respectively
        Methods :
            send_message : Sends the next message in the script
            make_daily_conclusion : Generates the daily conclusion
            make_final_conclusion : Generates the final conclusion
    """  # noqa: E501

    class startbot_command_flags(commands.FlagConverter):
        make_daily_conclusion_flag: typing.Optional[bool] = commands.flag(
            name="make_daily_conclusion_flag", default=True
        )
        make_final_conclusion_flag: typing.Optional[bool] = commands.flag(
            name="make_final_conclusion_flag", default=True
        )

    @commands.hybrid_command(name="start_bot", description="Start the bot")
    async def start_bot_command(self, ctx, *, flags: startbot_command_flags):
        await ctx.send("Starting the bot...")
        self.start_day_job.start()
        self.stop_day_job.start()

        self.day_nb = 1
        self.day_script = dataImport.CHAT_SCRIPT["day" + str(self.day_nb)][
            "script"
        ]
        self.message_nb = 0

        self.tools = self.bot.get_cog("Tools")
        await self.tools.set_global_ctx(ctx)

        self.make_daily_conclusion_flag = flags.make_daily_conclusion_flag
        self.make_final_conclusion_flag = flags.make_final_conclusion_flag

    class stopbot_command_flags(commands.FlagConverter):
        make_daily_conclusion_flag: typing.Optional[bool] = commands.flag(
            name="make_daily_conclusion_flag", default=True
        )
        make_final_conclusion_flag: typing.Optional[bool] = commands.flag(
            name="make_final_conclusion_flag", default=True
        )

    # stops the bot
    @commands.hybrid_command(name="stop_bot", description="Stop the bot")
    async def stop_bot_command(self, ctx, *, flags: stopbot_command_flags):
        await ctx.send("Stopping the bot...")
        self.start_day_job.stop()
        self.stop_day_job.stop()

        if flags.make_daily_conclusion_flag:
            await self.make_daily_conclusion()

        if flags.make_final_conclusion_flag:
            await self.make_final_conclusion()

    @commands.hybrid_command(name="start_day", description="Start the day")
    async def start_day(self, ctx):
        await self.start_day_job()

    @tasks.loop(
        time=dataImport.OPENING_CHANNEL_HOUR_TIMES,
        count=dataImport.SCRIPT_DAY_LENGTH,
    )
    async def start_day_job(self):
        self.day_nb += 1
        self.messages_job.start()

    @commands.hybrid_command(name="stop_day", description="Stop the day")
    async def stop_day(self, ctx):
        await self.stop_day_job()

    @tasks.loop(time=dataImport.CLOSING_CHANNEL_HOUR_TIMES)
    async def stop_day_job(self):
        self.messages_job.stop()

    @stop_day_job.after_loop  # After a day was finished
    async def after_stop_day_job(self):
        # If it is the last day
        if self.day_nb == dataImport.SCRIPT_DAY_LENGTH:
            # Make the final conclusion
            if self.make_final_conclusion_flag:
                await self.make_final_conclusion()
        else:
            # Make the daily conclusion
            if self.make_daily_conclusion_flag:
                await self.make_daily_conclusion(self.day_nb)

    @commands.hybrid_command(
        name="nextmessage", description="Send the next message"
    )
    async def send_message_command(self, ctx):
        await self.send_message()

    @tasks.loop(time=dataImport.MESSAGE_HOUR_TIMES)
    async def messages_job(self):
        # Send messages
        await self.send_message()

    async def send_message(self):
        # Looping
        if self.message_nb >= len(self.day_script):
            self.message_nb = 0

        # Get a message from the script
        ctx = await self.tools.get_global_ctx()
        await ctx.send(self.day_script[self.message_nb])

        self.message_nb += 1

    async def make_daily_conclusion(self) -> None:
        # If the extensions named "conclusionGenerator" is loaded
        if "extensions.conclusionGenerator" in self.bot.extensions:
            # Make the conclusion
            await self.bot.get_cog(
                "ConclusionGenerator"
            ).make_daily_conclusion(self.day_nb)
        else:
            print("ConclusionGenerator is not loaded")

    async def make_final_conclusion(self) -> None:
        # If the extensions named "conclusionGenerator" is loaded
        if "extensions.conclusionGenerator" in self.bot.extensions:
            # Make the conclusion
            await self.bot.get_cog(
                "ConclusionGenerator"
            ).make_final_conclusion()
        else:
            print("ConclusionGenerator is not loaded")


# Adding the cog to the bot
# Required to do this in order to use the commands
async def setup(bot) -> None:
    await bot.add_cog(DayManager(bot))
