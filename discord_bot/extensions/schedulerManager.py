"""
Cette classe ne doit être instanciée qu'une et une seule fois par objet forum
"""

import datetime

import modules.AnnouncementModule as AnnouncementModule
import modules.ReportModule as ReportModule
from discord.ext import commands, tasks

__all__ = ["SchedulerManager"]

UTC = datetime.timezone.utc

is_accelerated = True


class Scheduler:
    def __init__(self, bot: commands.Bot, forum):
        self.bot = bot
        self.forum = forum

    def get_config(self):
        return self.forum.config

    # Commence le forum
    async def start_forum(self) -> None:
        # Commence le premier jour
        config = self.get_config()
        config["GENERAL"]["CHANNELS"]["DAYS"][0]["IS_CURRENT_DAY"] = True

        # Envoie le message suivant
        days_config = await AnnouncementModule.send_next_message(
            config["GENERAL"]["CHANNELS"]["DAYS"],
            self.bot,
        )

        # Met à jour la config
        self.forum.set_days_config(days_config)

        # Lance les tâches à répétition
        # Tâche de messages à envoyer

        if is_accelerated:
            self.message_job.change_interval(seconds=3)
        else:
            messages_times = [
                datetime.time(hour=hour, tzinfo=UTC)
                for hour in config["GENERAL"]["MESSAGES_HOURS"]
            ]
            self.message_job.change_interval(time=messages_times)
        self.message_job.start()

        # - Changer de jour à chaque fin de journée
        if is_accelerated:
            self.day_job.change_interval(seconds=10)
        else:
            daily_close_time = datetime.time(
                hour=config["GENERAL"]["CLOSING_CHANNEL_HOUR"], tzinfo=UTC
            )
            self.day_job.change_interval(time=daily_close_time)
        self.day_job.start()

    async def next_day(self) -> None:
        # Récupère la configuration
        config = self.get_config()
        days_config = config["GENERAL"]["CHANNELS"]["DAYS"]
        nb_days = len(days_config)

        # Cherche le jour actuel
        for i in range(nb_days):
            if days_config[i]["IS_CURRENT_DAY"]:
                # Jour actuel trouvé

                # Fin de journée
                await AnnouncementModule.send_end_of_day_message(
                    days_config, self.bot
                )
                await ReportModule.generate_daily_report()

                days_config[i]["IS_CURRENT_DAY"] = False

                if i + 1 < nb_days:
                    # Si le jour suivant existe, on le passe à True
                    days_config[i + 1]["IS_CURRENT_DAY"] = True
                else:
                    # Dernier jour le script de fin de journée et le report
                    await AnnouncementModule.send_end_of_forum_message(
                        days_config, self.bot
                    )
                    await ReportModule.generate_forum_report()

                    # On arrête l'envoi de message et le changement de jour
                    self.message_job.cancel()
                    self.day_job.cancel()
                break

        # Met à jour la config
        self.forum.set_days_config(days_config)

    @tasks.loop()
    async def message_job(self) -> None:
        # Skip the first occurrence (whent starting the forum)
        if self.message_job.current_loop == 0:
            return
        # Récupère la configuration
        config = self.get_config()
        # Envoie le message suivant
        days_config = await AnnouncementModule.send_next_message(
            config["GENERAL"]["CHANNELS"]["DAYS"],
            self.bot,
        )
        # Met à jour la config
        self.forum.set_days_config(days_config)

    @tasks.loop()
    async def day_job(self) -> None:
        # Skip the first occurrence (whent starting the forum)
        if self.day_job.current_loop == 0:
            return
        await self.next_day()


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
