import discord
from discord.ext import commands, tasks
from dataclasses import dataclass

__all__ = ["privateChannels"]

@dataclass
class privateChannels(commands.Cog):
    bot: commands.Bot

    # EMBEDS
    # Les embeds sont des messages Discord particuliers dont l'affichage est différent des messages ordinaires.
    # Ils sont utiles pour différencier les messages utilisateurs des messages du bots et ressemblent davantage
    # à une interface d'application qu'à un message traditionnel.

    def embed_privateChannelMessage():
        embed=discord.Embed(title="Créer un canal privé", color=0x09b6e1)
        embed.add_field(name="Si tu souhaites témoigner mais que tu veux rester anonyme, si tu as besoin de nous contacter ou que tu recherches simplement un espace pour pouvoir vider ton sac, tu peux créer un canal privé !", value="", inline=False)
        embed.set_footer(text="Ce qui est dit dans les canaux privés n'est pas enregistré, sauf si tu donnes explicitement ton accord !")
        return embed


async def setup(bot) -> None:
    await bot.add_cog(privateChannels(bot))