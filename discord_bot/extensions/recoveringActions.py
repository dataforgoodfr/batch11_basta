import discord
from discord.ext import commands
from dataclasses import dataclass
import logging

from datetime import datetime

# Notes
# Lors de la création d'un thread, deux messages sont loggés
# modification du message original (pas du contenu), et "création" d'un nouveau message.
# entre guillemet car l'id reste le même, et le contenu n'est pas récupéré lors de l'action

@dataclass
class RecoveringActions(commands.Cog):
    bot: commands.Bot
    
    logger = logging.getLogger()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        This function is called everytime a message is sent in a channel the bot can see.
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

        config = self.bot.get_cog("ForumManager").get_forum(message.guild.id).config
        moderation_alert_channel_id = config["MODERATION"]["MODERATION_ALERTS_CHANNEL"]

        if channel_id in [moderation_alert_channel_id]:
            return

        logging.info(":".join([action, str(author_id), str(message_id), str(channel_id), str(thread_id), content]))

    @commands.Cog.listener()
    async def on_message_edit(self, message_before: discord.Message, message_after: discord.Message):
        """
        This function is called everytime a message is edited in a channel the bot can see.
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

        config = self.bot.get_cog("ForumManager").get_forum(message_after.guild.id).config
        moderation_alert_channel_id = config["MODERATION"]["MODERATION_ALERTS_CHANNEL"]

        if channel_id in [moderation_alert_channel_id]:
            return

        logging.info(":".join([action, str(author_id), str(message_id), str(channel_id), str(thread_id), new_content]))


    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """
        This function is called everytime a message is deleted in a channel the bot can see.
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
        
        config = self.bot.get_cog("ForumManager").get_forum(message.guild.id).config
        moderation_alert_channel_id = config["MODERATION"]["MODERATION_ALERTS_CHANNEL"]

        if channel_id in [moderation_alert_channel_id]:
            return

        logging.info(":".join([action, str(author_id), str(message_id), str(channel_id), str(thread_id), content]))
        
        

async def setup(bot) -> None:
    await bot.add_cog(RecoveringActions(bot))