from discord.ext import commands
from discord import Message

from dataclasses import dataclass, field

__all__ = ["ConclusionGenerator"]


@dataclass
class ConclusionGenerator(commands.Cog):
    bot: commands.Bot
    messages: list[Message] = field(default_factory=list)  # Store the messages

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        # ATTENTION, il recoit ses propres messages

        if message.author != self.bot.user and not message.content.startswith(
            ("!", "/", ".")
        ):
            self.messages.append(message)

    async def make_daily_conclusion(self) -> None:
        print("Making daily conclusion")

    async def make_final_conclusion(self) -> None:
        print("Making final conclusion")


# Adding the cog to the bot. It is required to do this in order to use the commands
async def setup(bot) -> None:
    await bot.add_cog(ConclusionGenerator(bot))
