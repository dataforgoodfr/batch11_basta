"""
Cette classe ne doit être instanciée qu'une et une seule fois par objet forum
"""

import logging
from datetime import datetime

import modules.AnnouncementModule as AnnouncementModule
import modules.PollModule as PollModule
import modules.ReportModule as ReportModule
import pytz
from discord.ext import commands, tasks

__all__ = ["SchedulerManager"]

is_accelerated = False


class Scheduler:
    def __init__(self, bot: commands.Bot, forum):
        self.bot = bot
        self.forum = forum

    # Passe au premier jour
    # Annonce le premier jour
    # Lance les tâches à répétition (ouverture, messages, fermeture)
    async def start_forum(self, ctx) -> None:
        config = self.forum.config
        # Si forum déjà lancé, on renvoi un message d'erreur
        if self.forum.config["GENERAL"]["CURRENT_DAY"] != -1:
            await AnnouncementModule.send_already_started_message(
                ctx, self.bot
            )
        else:
            # Commence le premier jour
            config["GENERAL"]["CURRENT_DAY"] = 0

            # Envoie un message de démarage
            await AnnouncementModule.send_start_of_forum_message(ctx, self.bot)

        # Lance les tâches à répétition :

        # Ouvrir les channels
        if is_accelerated:
            self.open_channels_job.change_interval(seconds=10)
        else:
            open_channels_time = [
                datetime.now()
                .replace(
                    hour=config["GENERAL"]["OPENING_CHANNEL_HOUR"],
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                .astimezone(pytz.utc)
                .time()
            ]
            self.open_channels_job.change_interval(time=open_channels_time)
        self.open_channels_job.start()

        # Messages à envoyer régulièrement
        if is_accelerated:
            self.message_job.change_interval(seconds=1)
        else:
            messages_times = [
                datetime.now()
                .replace(hour=hour, minute=0, second=0)
                .astimezone(pytz.utc)
                .time()
                for hour in config["GENERAL"]["MESSAGES_HOURS"]
            ]
            self.message_job.change_interval(time=messages_times)
        self.message_job.start()

        # Fermer les channels et passer au jour suivant
        if is_accelerated:
            self.close_channels_job.change_interval(seconds=9)
        else:
            close_channels_time = [
                datetime.now()
                .replace(
                    hour=config["GENERAL"]["CLOSING_CHANNEL_HOUR"],
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                .astimezone(pytz.utc)
                .time()
            ]
            self.close_channels_job.change_interval(time=close_channels_time)
        self.close_channels_job.start()

        # On ajoute le channel de modération dans les channels à ne pas report
        not_log_channels = self.forum.get_data("do_not_log_channels")
        if type(not_log_channels) is list:
            not_log_channels.append(
                config["MODERATION"]["MODERATION_ALERTS_CHANNEL"]
            )
        else:
            not_log_channels = [
                config["MODERATION"]["MODERATION_ALERTS_CHANNEL"]
            ]
        self.forum.save_data("do_not_log_channels", not_log_channels)

    # Envoi un message de fin de journée
    # Genère le rapport de la journée
    # Passe à la journée suivante ou fini le forum
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
                await self.end_forum()
        else:
            logging.warning("Le forum n'a pas encore commencé")

        # Met à jour la config
        self.forum.set_config(config)

    # Envoi un message de fin de forum
    # Récupère tous les sondages
    # Génère le rapport final
    async def end_forum(self) -> None:
        # Dernier jour le script de fin de journée et le report
        await AnnouncementModule.send_end_of_forum_message(
            self.forum.config, self.bot
        )
        await PollModule.fetch_polls(self.forum)
        await ReportModule.generate_forum_report(self.forum)

        # On arrête l'envoi de message et le changement de jour
        self.message_job.cancel()
        self.open_channels_job.cancel()
        self.close_channels_job.cancel()

        # On arrête le forum
        self.forum.config["GENERAL"]["CURRENT_DAY"] = -1

    # Tâches à répétition : envoi le message suivant
    @tasks.loop()
    async def message_job(self, manually=False) -> None:
        # A l'air de ne plus être utile

        # Skip the first occurrence (if the job was started and on first loop)
        # if not manually and self.message_job.current_loop == 0:
        #     return

        # Envoie le message suivant
        config = await AnnouncementModule.send_next_message(
            self.bot, self.forum
        )
        # Met à jour la config
        self.forum.set_config(config)

    # Tâches à répétition : ouvre les channels
    @tasks.loop()
    async def open_channels_job(self, manually=False) -> None:
        # A l'air de ne plus être utile

        # Skip the first occurrence (whent starting the forum)
        # if not manually and self.open_channels_job.current_loop == 0:
        #     return
        await self.forum.open_time_limited_channels()

    # Tâches à répétition : passe au jour suivant et ferme les channels
    @tasks.loop()
    async def close_channels_job(self, manually=False) -> None:
        # A l'air de ne plus être utile

        # Skip the first occurrence (whent starting the forum)
        # if not manually and self.close_channels_job.current_loop == 0:
        #     return
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

    @commands.hybrid_command(name="next_message")
    async def next_message(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            await self.get_forum(ctx.guild.id).scheduler.message_job(
                manually=True
            )
        else:
            await ctx.reply(
                "Vous n'avez pas le droit d'utiliser cette commande.",
                delete_after=10,
            )

    @commands.hybrid_command(name="end_day")
    async def end_day(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            await self.get_forum(ctx.guild.id).scheduler.close_channels_job(
                manually=True
            )
        else:
            await ctx.reply(
                "Vous n'avez pas le droit d'utiliser cette commande.",
                delete_after=10,
            )

    @commands.hybrid_command(name="start_day")
    async def start_day(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            await self.get_forum(ctx.guild.id).scheduler.open_channels_job(
                manually=True
            )
        else:
            await ctx.reply(
                "Vous n'avez pas le droit d'utiliser cette commande.",
                delete_after=10,
            )

    @commands.hybrid_command(name="end_forum")
    async def end_forum(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            await self.get_forum(ctx.guild.id).scheduler.end_forum()
        else:
            await ctx.reply(
                "Vous n'avez pas le droit d'utiliser cette commande.",
                delete_after=10,
            )


async def setup(bot) -> None:
    manager = SchedulerManager(bot)
    await bot.add_cog(manager)
