import discord
from discord.ext import commands, tasks
from dataclasses import dataclass

from datetime import datetime

__all__ = ["moderation"]

@dataclass
class Moderation(commands.Cog):
    bot: commands.Bot

    def embed_report(date, complaignant: discord.User, message: discord.Message):
        embed=discord.Embed(title="🚨 NOUVELLE ALERTE 🚨", color=0xff0000)
        embed.add_field(name="", value=f"**Date :** {date}\n **Plaignant :** {complaignant.mention}", inline=False)
        embed.add_field(name="Message signalé", value=f"Auteur : {message.author.mention}\n Canal : {message.channel.mention}\n Lien : {message.jump_url}\n Contenu : {message.content}", inline=False)
        return embed

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        if reaction.emoji == "🏴":
            await reaction.remove(user=user)
            forum = self.bot.get_cog("ForumManager").get_forum(reaction.message.guild.id)
            config = forum.config
            channel = reaction.message.guild.get_channel(config["GENERAL"]["CHANNELS"]["MODERATION_ALERTS_CHANNEL"])

            await channel.send(embed=Moderation.embed_report(str(datetime.now()), user, reaction.message))


async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))