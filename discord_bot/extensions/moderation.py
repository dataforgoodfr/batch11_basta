from discord.ext import commands, tasks
from dataclasses import dataclass

__all__ = ["moderation"]

@dataclass
class Moderation(commands.Cog):
    bot: commands.Bot


async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))