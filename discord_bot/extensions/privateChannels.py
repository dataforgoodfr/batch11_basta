import discord
from discord.ext import commands, tasks
from dataclasses import dataclass
import time

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
    
    def embed_welcome():
        embed=discord.Embed(title="🔒 Ton canal privé 🔒", description="Exprime-toi comme tu l'entends ! Tu peux ici témoigner anonymement, ou bien nous contacter si tu as besoin d'aide !", color=0x09b6e1)
        embed.add_field(name="🔗 Partager anonymement ton témoignage", value="> Ton témoignage peut apparaître dans le canal \"réponse anonyme\" du jour que tu souhaites ! Pour ce faire, clique simplement sur le jour auquel ton témoignage fait référence et suis les instructions.", inline=False)
        embed.set_footer(text="Le contenu de ce canal ne sera pas retenu dans la synthèse.")
        return embed
    
    def embed_share(day: int):
        embed=discord.Embed(title="▶️ Partager ton témoignage", color=0x1ae843)
        embed.add_field(name="", value=f"> Réagis avec '✅' aux messages que tu souhaites partager \n\n > Clique sur 'Confirmer le partage' et ton message sera partagé dans le canal de réponses anonymes du **Jour {day}** !", inline=False)
        return embed
    
    def embed_close():
        embed=discord.Embed(title="❌ Confirmer la suppression ❌ ", color=0xff0000)
        embed.add_field(name="Es-tu sûre de vouloir supprimer le canal ?", value="Toute suppression est définitive et irréversible. Les messages seront perdus.", inline=False)
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

        # /!\ CECI EST UN ATTRIBUT DE CLASSE. Il est accessible par toutes les instances mais il est unique.
        # Ainsi, le slow mode est général et pas seulement propre à un seul message avec des boutons.
        slow_mode = {}

        def __init__(self, day: int):
            super().__init__(timeout=None)
            self.add_item(self.ConfirmButton(label="Confirmer le partage", style=discord.ButtonStyle.primary, day=day))
            self.day = day

        @staticmethod
        async def get_messages(author, history):
            '''Returns a list with the messages the author reacted to using the checkmark emoji.'''
            message_list = []
            async for message in history:
                if message.author == author:
                    for reaction in message.reactions:
                        if reaction.emoji == "✅" and author in [user async for user in reaction.users()]:
                            message_list.append(message)
                            break
            message_list.reverse()
            return message_list
        
        class ConfirmButton(discord.ui.Button):
            def __init__(self, label, style, day):
                self.day = day
                custom_id=str(100 - day)
                super().__init__(label=label, style=style, custom_id=custom_id)
            
            async def callback(self, interaction: discord.Interaction):
                # SLOW MODE - Pour prévenir le spam dans le canal des réponses anonymes 
                if interaction.user.id in privateChannels.ConfirmShareButton.slow_mode.keys() and time.time() <= privateChannels.ConfirmShareButton.slow_mode[interaction.user.id]:
                    await interaction.response.send_message("Tu ne peux faire qu'un seul partage toutes les 15 minutes. Merci de patienter avant de pouvoir faire le prochain !", delete_after=30)
                    return
                
                message_list = await privateChannels.ConfirmShareButton.get_messages(interaction.user, interaction.channel.history(limit=100))

                if len(message_list) == 0:
                    await interaction.response.send_message("Tu n'as pas sélectionné de message !", delete_after=15)
                    return

                forum = interaction.client.get_cog("ForumManager").get_forum(interaction.guild.id)
                config = forum.config
                ano_answers = config["GENERAL"]["CHANNELS"]["DAYS"][self.day]["ANO_ANSWERS"]
                channel = interaction.guild.get_channel(ano_answers)

                embed=discord.Embed()
                embed.add_field(name="📢  Nouveau témoignage anonyme", value="", inline=False)
                await channel.send(embed=embed)
                for message in message_list:
                    await channel.send(message.content)

                await interaction.response.defer()
                await interaction.channel.send(f"✅ Ton témoignage a été partagé, {interaction.user.mention} !", delete_after=20)
                privateChannels.ConfirmShareButton.slow_mode[interaction.user.id] = time.time() + config["PRIVATE_CHANNELS"]["SHARING_COOLDOWN"]


    class ConfirmCloseButton(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Confirmer la suppression", style=discord.ButtonStyle.danger, custom_id="103")
        async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await interaction.channel.delete()

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
                await interaction.channel.send(embed=privateChannels.embed_share(int(self.custom_id)-1), view=privateChannels.ConfirmShareButton(day=int(self.custom_id)-2), delete_after=900)
                await interaction.response.defer()

        class RefreshButton(discord.ui.Button):
            def __init__(self, label, style, custom_id, disabled, bot):
                super().__init__(label=label, style=style, custom_id=custom_id, disabled=disabled)
                self.bot = bot

            async def callback(self, interaction: discord.Interaction):
                forum = self.bot.get_cog("ForumManager").get_forum(interaction.guild.id) # WARNING: BROKEN
                config = forum.config
                current_day = config["GENERAL"]["CURRENT_DAY"]
                await interaction.message.edit(view=privateChannels.ShareButtons(bot=self.bot, current_day=current_day))
                await interaction.response.defer()

        class CloseButton(discord.ui.Button):
            def __init__(self, label, style, custom_id, disabled):
                super().__init__(label=label, style=style, custom_id=custom_id, disabled=disabled)

            async def callback(self, interaction: discord.Interaction):
                await interaction.response.send_message(embed=privateChannels.embed_close(), view=privateChannels.ConfirmCloseButton(), delete_after=120)

        # La view crée 5 boutons "Jour 1", "Jour 2" etc. à l'initialisation.
        def __init__(self, bot, current_day=-1):
            super().__init__(timeout=None)
            for i in range(5):
                # Le décorateur utilisée dans la sous-classe PrivateChannelButton crée et ajoute automatiquement
                # le bouton à la view. Dans notre cas, vu que l'on déclare nous-même les objects ShareButton, il
                # est nécessaire de les ajouter manuellement à notre view.
                self.add_item(self.ShareButton(label=f"Jour {i+1}", style=discord.ButtonStyle.primary, custom_id=f"{i+2}", disabled=(i > current_day)))
            self.add_item(self.RefreshButton(label="🔄", style=discord.ButtonStyle.secondary, custom_id="101", disabled=False, bot=bot))
            # self.add_item(self.CloseButton(label="Fermer le canal", style=discord.ButtonStyle.danger, custom_id="102", disabled=False))

    # UTILS
    
    async def createPrivateChannel(interaction: discord.Interaction):
        '''Creates a private channel and sends the necessary information to properly use the channel.'''

        guild = interaction.guild # La 'guild' est la dénomination de discordpy pour représenter un serveur discord
        user = interaction.user # La personne qui demande la création d'un canal privé

        forum = interaction.client.get_cog("ForumManager").get_forum(guild.id)
        data = forum.get_data("privateChannels")

        if data == None:
            data = {}

        if "channels" in data.keys() and str(user.id) in data["channels"].keys():
            channel = guild.get_channel(data["channels"][str(user.id)])
            await channel.send(content=f"⚠️ Tu ne peux posséder qu'un seul canal privé, {user.mention}.", delete_after=20)
            return
        
        config = forum.config
        admin = guild.get_role(config["PRIVATE_CHANNELS"]["ADMIN_ROLE_ID"])

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            admin: discord.PermissionOverwrite(read_messages=True)
        } # Les overwrites permettent de changer les paramètres du canal au moment de sa création.

        if "counter" not in data.keys():
            data["counter"] = 0

        # Jour actuel
        current_day = config["GENERAL"]["CURRENT_DAY"]

        channel = await interaction.channel.category.create_text_channel(name="canal privé "+"{:04d}".format(data["counter"]), overwrites=overwrites)
        await channel.send(embed=privateChannels.embed_welcome(), view=privateChannels.ShareButtons(bot=interaction.client, current_day=current_day))
        await channel.send(f"✅ Ton canal personnel a été créé {interaction.user.mention} !", delete_after=20)

        data["counter"] = data["counter"] + 1

        if "channels" not in data.keys():
            data["channels"] = {}
        data["channels"][str(user.id)] = channel.id
        forum.save_data("privateChannels", data)

    # COMMANDS

    @commands.hybrid_command()
    async def generateprivatechannelmessage(self, ctx: commands.Context):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.interaction.response.send_message(
                "Vous n'avez pas le droit d'utiliser cette commande.",
                ephemeral=True,
                delete_after=10,
            )
            return
        embed = privateChannels.embed_privateChannelMessage()
        view = privateChannels.PrivateChannelButton()
        await ctx.send(embed=embed, view=view)


async def setup(bot) -> None:
    await bot.add_cog(privateChannels(bot))
    bot.add_view(privateChannels.PrivateChannelButton()) # Persistance du bouton "Créer un canal privé"
    bot.add_view(privateChannels.ShareButtons(bot=bot)) # Persistance des boutons de partage des jours
    # bot.add_view(privateChannels.ConfirmShareButton(day=0)) # LA DESACTIVATION EST VOLONTAIRE, voir issue #39
    for i in range(5):
        bot.add_view(privateChannels.ConfirmShareButton(day=i))
    bot.add_view(privateChannels.ConfirmCloseButton())
