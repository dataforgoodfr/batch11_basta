import os

import discord

# Finally, we're using extensions and Cogs as intented by discord.py
# https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
# Finally, we're using extensions and Cogs as intented by discord.py
# https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
from discord.ext import commands
from dotenv import load_dotenv
from helper.logger import setupLogger

# Bot class is specially designed for to create bots,
# so we use it instead of the Client class
# https://stackoverflow.com/questions/51234778/what-are-the-differences-between-bot-and-client

# We also choose to use the commands and tasks in order to run recurrent tasks
# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# https://discordpy.readthedocs.io/en/latest/ext/tasks/index.html


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
# Required to read users messages
intents.message_content = True

#Necessary to get a member from its id
intents.members = True 

bot = commands.Bot(command_prefix=".", intents=intents)


# be careful to load the extensions BEFORE running the bot
# /!\ WARNING: Keep an extra comma following the last extension name or it won't be loaded!
extensions = (
    "extensions.forumManager",
    "extensions.schedulerManager",
    "extensions.roleManager",
)

# Setup Logging
# We don't use the built-in logging system of discord.py
# because we want to have a custom logger that logs into a file and the stream
setupLogger()


@bot.event
async def setup_hook() -> None:
    for extension in extensions:
        await bot.load_extension(extension)


@bot.command(name="sync", description="Owner only")
async def sync(ctx):
    # Later replace by checking if user is admin
    if ctx.author.guild_permissions.administrator:
        # Syncing
        await ctx.bot.tree.sync()
        await ctx.reply("Syncing done !")
    else:
        await ctx.reply("You're not admin!")


# Always better if run at the end
# root_logger=True allow to run the python logger, not the one from discord.py
bot.run(BOT_TOKEN, root_logger=True)
