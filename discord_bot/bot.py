import discord

# Bot class is specially designed for to create bots so we use it instead of the Client class
# https://stackoverflow.com/questions/51234778/what-are-the-differences-between-bot-and-client

# We also choose to use the commands and tasks in order to run recurrent tasks
# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# https://discordpy.readthedocs.io/en/latest/ext/tasks/index.html

# Finally, we're using extensions and Cogs as intented by discord.py
# https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
from discord.ext import commands

import helpers.constantsImport as dataImport

intents = discord.Intents.default()
# Required to read users messages
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)


# be careful to load the extensions BEFORE running the bot
extensions = (
    "extensions.dayManager",
    "extensions.conclusionGenerator",
    "extensions.tools",
)


@bot.event
async def setup_hook() -> None:
    for extension in extensions:
        await bot.load_extension(extension)


@bot.command(name="sync", description="Owner only")
async def sync(ctx):
    # Later replace by checking if user is admin
    if ctx.author.id == 198894978737373184:
        # Syncing
        await ctx.bot.tree.sync()
        await ctx.reply("Syncing done !")
    else:
        await ctx.reply(f"You're not Augustin, your id is {ctx.author.id}")


# Always better if run at the end
bot.run(dataImport.BOT_TOKEN)
