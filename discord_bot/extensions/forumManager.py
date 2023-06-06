# CE FICHIER CONTIENT LA CLASSE MAÎTRESSE DU CHATBOT

import json
from os.path import exists
from shutil import copyfile
from typing import Tuple

from discord.ext import commands

from .schedulerManager import Scheduler

__all__ = ["ForumManager"]


# Un objet Forum par serveur
# Bizzare mais il n'a pas besoin d'hériter de commands.Cog pour créer des tasks
# ce qui nous arrange BEAUCOUP alors que dans la doc c'est dit que si
class Forum:
    def __init__(
        self,
        bot: commands.Bot,
        server_id: int,
        config: dict,
        config_filename: str,
    ):
        self.bot = bot
        self.server_id = server_id
        self.config = config
        self.config_filename = config_filename

    @classmethod  # FACTORY METHOD
    async def generate(cls, bot: commands.Bot, server_id: int):
        config, config_filename = Forum.find_config(server_id)
        forum = cls(bot, server_id, config, config_filename)
        scheduler = Scheduler(bot, forum)
        forum.scheduler = scheduler
        bot.get_cog("ForumManager").ACTIVE_FORUMS[server_id] = forum
        return forum

    @staticmethod
    def find_config(server_id: int) -> Tuple[dict, str]:
        config_filename = "./configurations/" + str(server_id) + ".json"

        if not exists(config_filename):
            copyfile("./configurations/template.json", config_filename)

        with open(config_filename) as config_file:
            config = json.load(config_file)

        return config, config_filename

    def set_config(self, config: dict):
        self.config = config
        # Write the config to the file
        with open(self.config_filename, "w") as config_file:
            json.dump(config, config_file, indent=4)

    def set_days_config(self, days_config: dict):
        self.config["GENERAL"]["CHANNELS"]["DAYS"] = days_config
        self.set_config(self.config)


# Un objet pour le bot, chargé de gérer les objets Forum
class ForumManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Dict {'ID du serveur' : 'Objet Forum associé'}
        self.ACTIVE_FORUMS = {}

    def get_forums(self):
        return self.ACTIVE_FORUMS

    def get_forum(self, server_id: int):
        return (
            self.ACTIVE_FORUMS[server_id]
            if server_id in self.ACTIVE_FORUMS.keys()
            else None
        )

    async def reload(self):
        async for guild in self.bot.fetch_guilds():
            if guild.id not in self.ACTIVE_FORUMS.keys():
                # Voir si passer seulement l'ID suffit où si il y a un gain à
                # passer l'objet guild entièrement
                await Forum.generate(self.bot, guild.id)

    @commands.hybrid_command(
        name="load_forums",
        description="Génère des objets forums et des \
        fichiers de configuration pour les serveurs sans",
    )
    async def load_configs(self, ctx: commands.Context):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.interaction.response.send_message(
                "Vous n'avez pas le droit d'utiliser cette commande.",
                ephemeral=True,
                delete_after=10,
            )
            return
        await self.reload()
        await ctx.send("Done!", delete_after=5)

    @commands.hybrid_command(
        name="reload_config",
        description="Recharge la configuration en fonction du contenu \
            du fichier JSON associé.",
    )
    async def reload_config(self, ctx: commands.Context):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.interaction.response.send_message(
                "Vous n'avez pas le droit d'utiliser cette commande.",
                ephemeral=True,
                delete_after=10,
            )
            return
        if ctx.guild.id in self.ACTIVE_FORUMS.keys():
            forum = self.ACTIVE_FORUMS[ctx.guild.id]
            forum.load_config()
            await ctx.send("Done!", delete_after=5)
        else:
            await ctx.send(
                "Erreur: pas d'objet Forum pour ce serveur - \
                pas de configuration associée ; utilisez _/load_configs_."
            )

    # Lorsque le bot rejoint un nouveau serveur
    # -> créer un objet Forum (et une configuration associée)
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await Forum.generate(self.bot, guild.id)


async def setup(bot) -> None:
    manager = ForumManager(bot)
    await bot.add_cog(manager)
    await manager.reload()
