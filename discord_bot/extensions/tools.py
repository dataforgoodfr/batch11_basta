from dataclasses import dataclass
from discord.ext import commands

__all__ = ["Tools"]


@dataclass
class Tools(commands.Cog):
    bot: commands.Bot

    global_ctx = None

    async def send_message(self, message, ctx = None):
        ctx = ctx or self.global_ctx
        await ctx.send(message)

    async def set_global_ctx(self, ctx):
        self.global_ctx = ctx
    
    async def get_global_ctx(self):
        return self.global_ctx

    
# Adding the cog to the bot. It is required to do this in order to use the commands
async def setup(bot) -> None:
    await bot.add_cog(Tools(bot))