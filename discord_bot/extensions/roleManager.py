import discord
from discord.ext import commands, tasks
from dataclasses import dataclass

from datetime import datetime

__all__ = ["roleManager"]

@dataclass
class RoleManager(commands.Cog):
    bot: commands.Bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        forum = self.bot.get_cog("ForumManager").get_forum(reaction.message.guild.id)
        config = forum.config
        if reaction.message.id == config["ROLE_MANAGER"]["RULE_MESSAGE_ID"]:
            if reaction.emoji == "✅":
                base_role = reaction.message.guild.get_role(config["ROLE_MANAGER"]["BASE_ROLE_ID"])
                if base_role not in user.roles:
                    user.add_roles()


async def setup(bot) -> None:
    await bot.add_cog(RoleManager(bot))