import discord
from discord.ext import commands, tasks
from dataclasses import dataclass

__all__ = ["privateChannels"]

# CONFIGURATION
ADMIN_ROLE_ID = 1100893370248876092

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
    

    # UTILS
    
    async def createPrivateChannel(interaction: discord.Interaction):
        '''Creates a private channel and sends the necessary information to properly use the channel.'''

        guild = interaction.guild # La 'guild' est la dénomination de discordpy pour représenter un serveur discord
        user = interaction.user # La personne qui demande la création d'un canal privé
        admin = guild.get_role(ADMIN_ROLE_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            admin: discord.PermissionOverwrite(read_messages=True)
        } # Les overwrites permettent de changer les paramètres du canal au moment de sa création.

        channel = await interaction.channel.category.create_text_channel("canal privé XXXX", overwrites=overwrites)
        await channel.send(f"Bienvenue {interaction.user.mention}, ici tu peux t'exprimer comme tu l'entends.")


async def setup(bot) -> None:
    await bot.add_cog(privateChannels(bot))