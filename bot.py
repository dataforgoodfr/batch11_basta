import discord

# Bot command framework is specially designed for to create bots
# Doc : https://discordpy.readthedocs.io/en/stable/ext/commands/
from discord.ext import commands

import typing

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
# Required to read users messages
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)


class test_command_flags(commands.FlagConverter):
    sentence: typing.Optional[str] = commands.flag(
        description="Insert here the bot response."
    )


@bot.hybrid_command(
    name="testopt", description="Test command with an optional argument"
)
async def testOpt(ctx, *, flags: test_command_flags):
    if flags.sentence:
        await ctx.reply(flags.sentence)

    await ctx.send(f"Test done !")


@bot.command(name="sync", description="Owner only")
async def sync(ctx):
    # Later replace by checking if user is admin
    if ctx.author.id == 198894978737373184:
        # Syncing
        await ctx.bot.tree.sync()
        await ctx.reply("Syncing done !")
    else:
        await ctx.reply(f"You're not Augustin, your id is {ctx.author.id}")


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    print(
        f"{message.channel}: {message.author}: {message.author.name}: {message.content}"
    )

    if message.author == bot.user:  # Won't track its own messages
        return

    # Extremely important to call this. Otherwise, the bot will not respond to commands because no processing is done on the message.
    await bot.process_commands(message)


bot.run(BOT_TOKEN)
