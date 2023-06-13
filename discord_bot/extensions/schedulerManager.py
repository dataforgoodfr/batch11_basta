"""
Cette classe ne doit être instanciée qu'une et une seule fois par objet forum
"""

import datetime
import logging

import modules.AnnouncementModule as AnnouncementModule
import modules.PollModule as PollModule
import modules.ReportModule as ReportModule
from discord.ext import commands, tasks

__all__ = ["SchedulerManager"]

UTC = datetime.timezone.utc

is_accelerated = False


class Scheduler:
    def __init__(self, bot: commands.Bot, forum):
        self.bot = bot
        self.forum = forum

    # Commence le forum
    async def start_forum(self, ctx) -> None:
        # Si forum déjà lancé, on renvoi un message d'erreur
        if self.forum.config["GENERAL"]["CURRENT_DAY"] != -1:
            await AnnouncementModule.send_already_started_message(
                ctx, self.bot
            )
            return

        # Commence le premier jour
        config = self.forum.config
        config["GENERAL"]["CURRENT_DAY"] = 0

        # Envoie un message de démarage
        await AnnouncementModule.send_start_of_forum_message(ctx, self.bot)

        # Lance les tâches à répétition :

        # Ouvrir les channels
        if is_accelerated:
            self.open_channels_job.change_interval(seconds=10)
        else:
            open_channels_time = datetime.time(
                hour=config["GENERAL"]["OPENING_CHANNEL_HOUR"], tzinfo=UTC
            )
            self.open_channels_job.change_interval(time=open_channels_time)
        self.open_channels_job.start()

        # Messages à envoyer régulièrement
        if is_accelerated:
            self.message_job.change_interval(seconds=1)
        else:
            messages_times = [
                datetime.time(hour=hour, tzinfo=UTC)
                for hour in config["GENERAL"]["MESSAGES_HOURS"]
            ]
            self.message_job.change_interval(time=messages_times)
        self.message_job.start()

        # Fermer les channels et passer au jour suivant
        if is_accelerated:
            self.close_channels_job.change_interval(seconds=9)
        else:
            close_channels_time = datetime.time(
                hour=config["GENERAL"]["CLOSING_CHANNEL_HOUR"], tzinfo=UTC
            )
            self.close_channels_job.change_interval(time=close_channels_time)
        self.close_channels_job.start()

    async def next_day(self) -> None:
        # Récupère la configuration
        config = self.forum.config
        nb_days = len(config["GENERAL"]["CHANNELS"]["DAYS"])

        jour_actuel = config["GENERAL"]["CURRENT_DAY"]
        if jour_actuel != -1:
            # forum commencé

            # Annonce de fin de journée et génération du rapport
            await AnnouncementModule.send_end_of_day_message(config, self.bot)
            await ReportModule.generate_daily_report(self.forum)

            if jour_actuel < nb_days - 1:
                # Si le jour suivant existe, on le passe
                jour_actuel += 1
                config["GENERAL"]["CURRENT_DAY"] = jour_actuel
            else:
                # Dernier jour le script de fin de journée et le report
                await AnnouncementModule.send_end_of_forum_message(
                    config, self.bot
                )
                await PollModule.fetch_polls(self.forum)
                await ReportModule.generate_forum_report(self.forum)

                # On arrête l'envoi de message et le changement de jour
                self.message_job.cancel()
                self.open_channels_job.cancel()
                self.close_channels_job.cancel()

                # On arrête le forum
                config["GENERAL"]["CURRENT_DAY"] = -1
        else:
            logging.warning("Le forum n'a pas encore commencé")

        # Met à jour la config
        self.forum.set_config(config)

    @tasks.loop()
    async def message_job(self) -> None:
        # Skip the first occurrence (whent starting the forum)
        if self.message_job.current_loop == 0:
            return
        # Envoie le message suivant
        config = await AnnouncementModule.send_next_message(
            self.bot, self.forum
        )
        # Met à jour la config
        self.forum.set_config(config)

    @tasks.loop()
    async def open_channels_job(self) -> None:
        # Skip the first occurrence (whent starting the forum)
        if self.open_channels_job.current_loop == 0:
            return
        await self.forum.open_time_limited_channels()

    @tasks.loop()
    async def close_channels_job(self) -> None:
        # Skip the first occurrence (whent starting the forum)
        if self.close_channels_job.current_loop == 0:
            return
        await self.next_day()
        await self.forum.close_time_limited_channels()


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
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.interaction.response.send_message(
                "Vous n'avez pas le droit d'utiliser cette commande.",
                ephemeral=True,
                delete_after=10,
            )
            return
        # Get the scheduler associated with the server
        forum = self.get_forum(ctx.guild.id)
        scheduler = forum.scheduler
        await scheduler.start_forum(ctx)

    @commands.hybrid_command(name="open_channels")
    async def open_channels(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            forum = self.get_forum(ctx.guild.id)
            await forum.open_time_limited_channels()
        else:
            await ctx.reply(
                "Vous n'avez pas le droit d'utiliser cette commande.",
                delete_after=10,
            )

    @commands.hybrid_command(name="close_channels")
    async def close_channels(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            forum = self.get_forum(ctx.guild.id)
            await forum.close_time_limited_channels()
        else:
            await ctx.reply(
                "Vous n'avez pas le droit d'utiliser cette commande.",
                delete_after=10,
            )

    @commands.hybrid_command(name="generate_end_report")
    async def generate_end_report(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            await ReportModule.generate_forum_report(
                self.get_forum(ctx.guild.id)
            )
        else:
            await ctx.reply(
                "Vous n'avez pas le droit d'utiliser cette commande.",
                delete_after=10,
            )


async def setup(bot) -> None:
    manager = SchedulerManager(bot)
    await bot.add_cog(manager)
