import logging
from dataclasses import dataclass

import discord
from discord.ext import commands

"""
NOTE :
Les threads sont bien logged, seuulement, les threads pouvant être créés
de deux manières différentes, chaque scénario propose un pattern unique :
  1. Scénario duu thread créé par clic-droit -> "Créer un fil" sur un message :
    1. EDITION : Le message sur le channel utilisé pour créer le thread.
    Le contenu ne change pas.
    2. CRÉATION : création du premier message dans le thread.
    Cependant, le contenu n'est pas récupéré et le message "Sorry,
    we couldn't load the first message in this thread" est retourné
    3. CRÉATION : Ajout du premier message utilisé par l'utilisateur
    pour lancer le thread. Le contenu est récupéré normalement.
  2. Scénario du thread créé par l'option + -> "Créer un fil" sur un channel :
    1. CRÉATION : Un message intitulé "[user.name] started a thread:
    **New threads**. See all **threads**." est créé sur le channel.
    2. EDITION : Ce même message sur le channel est édité.
    Le contenu ne change pas.
    3. CRÉATION : Ajout du premier message utilisé par l'utilisateur
    pour lancer le thread. Le contenu est récupéré normalement.

TODO :
- Utiliser les listener raw pour récupérer les messages édités et supprimés
qui ne sont pas dans le cache
"""


@dataclass
class RecoveringActions(commands.Cog):
    bot: commands.Bot

    logger = logging.getLogger()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        This function is called everytime a message is sent
        in a channel the bot can see.
        """

        action = "NEW_MESSAGE"
        message_id = message.id
        author_id = message.author.id
        content = message.system_content
        channel = message.channel
        if type(channel) == discord.Thread:
            thread_id = channel.id
            channel_id = channel.parent.id
        else:
            thread_id = None
            channel_id = channel.id

        # Bout de code commenté car obsolète
        # Raison : On veut logger tous les messages/actions,
        # la modération se fera à la génération de la synthèse

        # config = (
        #     self.bot.get_cog("ForumManager").get_forum(message.guild.id).config
        # )
        # moderation_alert_channel_id = config["MODERATION"][
        #     "MODERATION_ALERTS_CHANNEL"
        # ]

        # if channel_id in [moderation_alert_channel_id]:
        #     return

        logging.info(
            ":".join(
                [
                    action,
                    str(author_id),
                    str(message_id),
                    str(channel_id),
                    str(thread_id),
                    content,
                ]
            )
        )

    @commands.Cog.listener()
    async def on_message_edit(
        self, message_before: discord.Message, message_after: discord.Message
    ):
        """
        This function is called everytime a message is edited
        in a channel the bot can see.
        """

        # Ne marche pas dans les threads

        action = "EDIT_MESSAGE"
        message_id = message_after.id
        author_id = message_after.author.id
        new_content = message_after.system_content

        channel = message_after.channel
        if type(channel) == discord.Thread:
            thread_id = channel.id
            channel_id = channel.parent.id
        else:
            thread_id = None
            channel_id = channel.id

        config = (
            self.bot.get_cog("ForumManager")
            .get_forum(message_after.guild.id)
            .config
        )
        moderation_alert_channel_id = config["MODERATION"][
            "MODERATION_ALERTS_CHANNEL"
        ]

        if channel_id in [moderation_alert_channel_id]:
            return

        logging.info(
            ":".join(
                [
                    action,
                    str(author_id),
                    str(message_id),
                    str(channel_id),
                    str(thread_id),
                    new_content,
                ]
            )
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """
        This function is called everytime a message is deleted
        in a channel the bot can see.
        """

        # Ne marche pas dans les threads

        action = "DELETE_MESSAGE"
        message_id = message.id
        author_id = message.author.id
        content = message.system_content

        channel = message.channel
        if type(channel) == discord.Thread:
            thread_id = channel.id
            channel_id = channel.parent.id
        else:
            thread_id = None
            channel_id = channel.id

        config = (
            self.bot.get_cog("ForumManager").get_forum(message.guild.id).config
        )
        moderation_alert_channel_id = config["MODERATION"][
            "MODERATION_ALERTS_CHANNEL"
        ]

        if channel_id in [moderation_alert_channel_id]:
            return

        logging.info(
            ":".join(
                [
                    action,
                    str(author_id),
                    str(message_id),
                    str(channel_id),
                    str(thread_id),
                    content,
                ]
            )
        )


async def setup(bot) -> None:
    await bot.add_cog(RecoveringActions(bot))
