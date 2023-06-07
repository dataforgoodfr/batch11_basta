import discord
from discord.ext import commands, tasks
from dataclasses import dataclass

from datetime import datetime

__all__ = ["roleManager"]

@dataclass
class RoleManager(commands.Cog):
    bot: commands.Bot

    @commands.Cog.listener()
    # 'on_raw_reaction_add()' est appelé à chaque ajout de réaction, indépendamment de l'état du message dans le cache du bot.
    # C'est utile puisque si on utilisait 'on_reaction_add()', le bot ne serait pas notifié lors de l'ajout d'une réaction
    # à un message envoyé avant qu'il soit lancé.
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        forum = self.bot.get_cog("ForumManager").get_forum(payload.guild_id)
        config = forum.config
        if payload.message_id == config["ROLE_MANAGER"]["RULE_MESSAGE_ID"]:
            if str(payload.emoji) == "✅":
                guild = self.bot.get_guild(payload.guild_id)
                base_role = guild.get_role(config["ROLE_MANAGER"]["BASE_ROLE_ID"])
                if base_role not in payload.member.roles:
                    await payload.member.add_roles(base_role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        forum = self.bot.get_cog("ForumManager").get_forum(payload.guild_id)
        config = forum.config
        if payload.message_id == config["ROLE_MANAGER"]["RULE_MESSAGE_ID"]:
            if str(payload.emoji) == "✅":
                guild = self.bot.get_guild(payload.guild_id)
                base_role = guild.get_role(config["ROLE_MANAGER"]["BASE_ROLE_ID"])
                # Le payload renvoyé par 'on_raw_reaction_remove()' ne contient pas de champ payload.member.
                # Il est donc nécessaire de le récupérer à la main, via l'ID de l'utilisateur.
                member = guild.get_member(162227524498096128)
                if base_role in member.roles:
                    await member.remove_roles(base_role)


async def setup(bot) -> None:
    await bot.add_cog(RoleManager(bot))