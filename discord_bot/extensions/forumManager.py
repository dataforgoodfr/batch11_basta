# CE FICHIER CONTIENT LA CLASSE MAÎTRESSE DU CHATBOT

from discord.ext import tasks, commands

import json
from os.path import exists
from shutil import copyfile
from datetime import timezone, time

__all__ = ["forumManager"]

ACTIVE_FORUMS = {} # Ce dictionnaire fait le lien entre 'ID du serveur' -> 'Objet Forum associé'

def get_forums():
    return ACTIVE_FORUMS

def get_forum(server_id: int):
    return ACTIVE_FORUMS[server_id] if server_id in ACTIVE_FORUMS.keys() else None
    
# Un objet Forum par serveur
class Forum():
    
    def __init__(self, bot: commands.Bot, server_id: int):
        self.bot = bot
        self.server_id = server_id

    def load_config(self):

        # TODO: sécurité?

        config_filename = "./configurations/"+str(self.server_id)+".json"

        if not exists(config_filename):
            copyfile("./configurations/template.json", config_filename)

        with open(config_filename) as config_file:
            self.CONFIG = json.load(config_file)

    def get_config(self):
        return self.CONFIG

    def generate(bot: commands.Bot, server_id: int): # FACTORY METHOD
        forum = Forum(bot, server_id)
        ACTIVE_FORUMS[server_id] = forum

        forum.load_config()

        return forum


# Un objet pour le bot, chargé de gérer les objets Forum
class ForumManager(commands.Cog):

    async def reload(self):
        async for guild in self.bot.fetch_guilds():
            if guild.id not in ACTIVE_FORUMS.keys():
                Forum.generate(self.bot, guild.id) # Voir si passer seulement l'ID suffit où si il y a un gain à passer l'objet guild entièrement 

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        



async def setup(bot) -> None:
    manager = ForumManager(bot)
    await bot.add_cog(manager)
    await manager.reload()