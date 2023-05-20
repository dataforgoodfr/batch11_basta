# CE FICHIER CONTIENT LA CLASSE MAÎTRESSE DU CHATBOT

from discord.ext import tasks, commands

from json import load
from datetime import timezone, time

__all__ = ["forumManager"]

ACTIVE_FORUMS = {} # Ce dictionnaire fait le lien entre 'ID du serveur' -> 'Objet Forum associé'

# Un objet Forum par serveur
class Forum():
    
    def __init__(self, bot: commands.Bot, server_id: int):
        self.bot = bot
        self.server_id = server_id

    def generate(bot: commands.Bot, server_id: int): # FACTORY METHOD
        forum = Forum(bot)
        ACTIVE_FORUMS[server_id] = forum


# Un objet pour le bot, chargé de gérer les objets Forum
class ForumManager(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    


async def setup(bot) -> None:
    await bot.add_cog(ForumManager(bot))