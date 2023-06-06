import discord
from discord.ext import commands, tasks
from dataclasses import dataclass
import time

__all__ = ["privateChannels"]

# CONFIGURATION
ADMIN_ROLE_ID = 1100893370248876092
CURRENT_DAY = 3 # Temporaire

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
    

    # VIEWS
    # Les views permettent de créer des dispositions de 'components' Discord. Dans notre cas, elles sont utiles
    # pour pouvoir ajouter des boutons aux messages du bot, et rendre les interactions plus pratiques qu'avec des réactions.
    # Elles permettent aussi de gérer plus facilement les interactions qu'avec des récations.

    class PrivateChannelButton(discord.ui.View):

        def __init__(self):
           super().__init__(timeout=None) # Il est nécessaire d'explicitement définir le timeout à None pour permettre la persistance

        # Ce décorateur permet de déclarer la création d'un bouton, et la méthode 'button' est appelée lorsque le bouton est cliqué.
        # /!\ IMPORTANT /!\ - Le champ "custom_id" permet la persistance des boutons. C'est-à-dire que les boutons fonctionneront
        #                     encore après que le bot est redémarré. C'est très important puisque sans cette persistance, il serait
        #                     nécessaire que le bot réécrive son message à chaque lancement pour pouvoir générer des boutons fonctionnels. 
        @discord.ui.button(label="Créer un canal privé",style=discord.ButtonStyle.primary, custom_id="1")
        async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await privateChannels.createPrivateChannel(interaction)
            await interaction.response.defer() # Marque l'interaction comme terminée pour éviter des messages "L'interaction a échoué"
    
    class ConfirmShareButton(discord.ui.View):

        def __init__(self):
            super().__init__(timeout=None)
            self.slow_mode = {}

        @staticmethod
        async def get_messages(author, history):
            '''Returns a list with the messages the author reacted to using the checkmark emoji.'''
            message_list = []
            async for message in history:
                if message.author == author:
                    for reaction in message.reactions: # TODO: optimisation
                        if reaction.emoji == "✅" and author in [user async for user in reaction.users()]:
                            message_list.append(message)
                            break
            message_list.reverse()
            return message_list

        @discord.ui.button(label="Confirmer le partage", style=discord.ButtonStyle.primary, custom_id="100")
        async def button(self, interaction: discord.Interaction, button: discord.ui.Button):

            # SLOW MODE - Pour prévenir le spam dans le canal des réponses anonymes 
            if interaction.user.id in self.slow_mode.keys() and time.time() <= self.slow_mode[interaction.user.id]:
                await interaction.response.send_message("Vous ne pouvez faire qu'un seul partage toutes les 15 minutes. Merci de patienter avant de pouvoir faire le prochain !", delete_after=30)
                return
            
            await interaction.response.defer()
            message_list = await self.get_messages(interaction.user, interaction.channel.history(limit=100))

            forum = interaction.client.get_cog("ForumManager").get_forum(interaction.guild.id)
            config = forum.config
            ano_answers = config["GENERAL"]["CHANNELS"]["DAYS"][0]["ANO_ANSWERS"] #TODO: get current_day
            channel = interaction.guild.get_channel(ano_answers)

            for message in message_list:
                await channel.send(message.content)

            self.slow_mode[interaction.user.id] = time.time() + config["PRIVATE_CHANNELS"]["SHARING_COOLDOWN"]

    class ShareButtons(discord.ui.View):

        # Cette sous-classe de bouton permettra de créer les boutons "Jour 1, "Jour 2" etc.
        # On utilise une sous-classe puisque l'on souhaite créer des boutons avec des noms différents mais
        # avec un comportement similaire.
        class ShareButton(discord.ui.Button):
            def __init__(self, label, style, custom_id, disabled):
                super().__init__(label=label, style=style, custom_id=custom_id, disabled=disabled)
                # Le tag 'disabled' permet de désactiver les boutons (ie. de les afficher sans qu'ils soient cliquables).
                # Les boutons correspondant à des jours non ouverts sont désactivés.
            
            async def callback(self, interaction: discord.Interaction):
                await interaction.response.send_message(f"yes {self.label}") # Temporaire
                await interaction.channel.send(f"channel: {interaction.channel.id}")
                await interaction.channel.send("Allez", view=privateChannels.ConfirmShareButton())

        class RefreshButton(discord.ui.Button):
            def __init__(self, label, style, custom_id, disabled):
                super().__init__(label=label, style=style, custom_id=custom_id, disabled=disabled)

            async def callback(self, interaction: discord.Interaction):
                await interaction.message.edit(view=privateChannels.ShareButtons(current_day=5)) #TODO: current day
                await interaction.response.defer()

        # La view crée 5 boutons "Jour 1", "Jour 2" etc. à l'initialisation.
        def __init__(self, current_day=3):
            super().__init__(timeout=None)
            for i in range(5):
                # Le décorateur utilisée dans la sous-classe PrivateChannelButton crée et ajoute automatiquement
                # le bouton à la view. Dans notre cas, vu que l'on déclare nous-même les objects ShareButton, il
                # est nécessaire de les ajouter manuellement à notre view.
                self.add_item(self.ShareButton(label=f"Jour {i+1}", style=discord.ButtonStyle.primary, custom_id=f"{i+2}", disabled=(i+1 > current_day)))
            self.add_item(self.RefreshButton(label="🔄", style=discord.ButtonStyle.secondary, custom_id="101", disabled=False))

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
        await channel.send("Partage :)", view=privateChannels.ShareButtons())

    # COMMANDS

    @commands.hybrid_command()
    async def generateprivatechannelmessage(self, ctx):
        embed = privateChannels.embed_privateChannelMessage()
        view = privateChannels.PrivateChannelButton()
        await ctx.send(embed=embed, view=view)


async def setup(bot) -> None:
    await bot.add_cog(privateChannels(bot))
    bot.add_view(privateChannels.PrivateChannelButton()) # Persistance du bouton "Créer un canal privé"
    bot.add_view(privateChannels.ShareButtons()) # Persistance des boutons de partage des jours
    bot.add_view(privateChannels.ConfirmShareButton())
