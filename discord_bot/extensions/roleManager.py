import discord
from discord.ext import commands, tasks
from dataclasses import dataclass

from datetime import datetime

__all__ = ["roleManager"]

@dataclass
class RoleManager(commands.Cog):
    bot: commands.Bot

    


async def setup(bot) -> None:
    await bot.add_cog(RoleManager(bot))