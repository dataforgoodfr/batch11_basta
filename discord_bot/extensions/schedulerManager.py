"""
Cette classe ne doit être instanciée qu'une et une seule fois par objet forum
"""

import modules.AnnouncementModule as AnnouncementModule
from discord.ext import commands

__all__ = ["SchedulerManager"]


class Scheduler:
    def __init__(self, bot: commands.Bot, forum):
        self.bot = bot
        self.forum = forum

    # Commence le forum
    async def start_forum(self) -> None:
        # Commence le premier jour
        config = self.forum.config
        config["GENERAL"]["CHANNELS"]["DAYS"][0]["IS_CURRENT_DAY"] = True

        # Envoie le message suivant
        days_config = await AnnouncementModule.send_next_message(
            config["GENERAL"]["CHANNELS"]["DAYS"],
            self.bot,
        )

        # Met à jour la config
        self.forum.set_days_config(days_config)

        # Lance les tâches à répétition :
        # - Envoyer un message à chaque heures de la config
        # - Changer de jour à chaque fin de journée


class SchedulerManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Cette classe ne sert seulement qu'à récupérer les commandes liées au
    # scheduler puis à les transmettre au bon scheduler

    def get_ForumManager(self):
        return self.bot.get_cog("ForumManager")

    def get_forum(self, server_id: int):
        return self.get_ForumManager().get_forum(server_id)

    @commands.hybrid_command(
        name="start_forum",
        description="Lance le forum ainsi avec les configurations chargées",
    )
    async def start_forum(self, ctx: commands.Context) -> None:
        # Get the scheduler associated with the server
        forum = self.get_forum(ctx.guild.id)
        scheduler = forum.scheduler
        await scheduler.start_forum()


async def setup(bot) -> None:
    manager = SchedulerManager(bot)
    await bot.add_cog(manager)
