import discord
from discord.ext import commands, tasks
from dataclasses import dataclass

__all__ = ["privateChannels"]

@dataclass
class privateChannels(commands.Cog):
    bot: commands.Bot

    # CLASS CONTENT


async def setup(bot) -> None:
    await bot.add_cog(privateChannels(bot))