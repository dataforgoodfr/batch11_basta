import discord
from discord.ext import commands, tasks
from dataclasses import dataclass

from datetime import datetime

__all__ = ["roleManager"]

@dataclass
class RoleManager(commands.Cog):
    bot: commands.Bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        forum = self.bot.get_cog("ForumManager").get_forum(payload.guild_id)
        config = forum.config
        if payload.message_id == config["ROLE_MANAGER"]["RULE_MESSAGE_ID"]:
            if str(payload.emoji) == "✅":
                guild = self.bot.get_guild(payload.guild_id)
                base_role = guild.get_role(config["ROLE_MANAGER"]["BASE_ROLE_ID"])
                if base_role not in payload.member.roles:
                    await payload.member.add_roles(base_role)


async def setup(bot) -> None:
    await bot.add_cog(RoleManager(bot))