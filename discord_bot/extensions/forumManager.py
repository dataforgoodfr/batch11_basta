# CE FICHIER CONTIENT LA CLASSE MAÎTRESSE DU CHATBOT

import json
from os.path import exists
from shutil import copyfile
from typing import Tuple

import discord
import modules.AnnouncementModule as AnnouncementModule
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
        self.is_running = False

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

    # Allow user @everyone to send messages in the channels
    async def open_time_limited_channels(self):
        channels_ids = self.config["GENERAL"]["TIME_RESTRICTED_CHANNELS"]
        for channel_id in channels_ids:
            channel = self.bot.get_channel(channel_id)
            await channel.set_permissions(
                self.bot.get_guild(self.server_id).default_role,
                send_messages=True,
            )
        await AnnouncementModule.send_opening_messages(channels_ids, self.bot)

    # Disallow user @everyone to send messages in the channels
    async def close_time_limited_channels(self):
        channels_ids = self.config["GENERAL"]["TIME_RESTRICTED_CHANNELS"]
        for channel_id in channels_ids:
            channel = self.bot.get_channel(channel_id)
            await channel.set_permissions(
                self.bot.get_guild(self.server_id).default_role,
                send_messages=False,
            )
        await AnnouncementModule.send_closing_messages(channels_ids, self.bot)


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

    @commands.hybrid_command(
        name="poll",
        description="Lance un sondage",
    )
    async def poll(self, ctx, multivote: bool, question, options: str):
        options = options.split(",")
        if len(options) <= 1:
            await ctx.send("You need more than one option to make a poll!")
            return
        if len(options) > 10:
            await ctx.send("You cannot make a poll for more than 10 things!")
            return

        if len(options) == 2 and (
            (options[0].lower, options[1].lower) == ("oui", "non")
            or (options[0].lower, options[1].lower) == ("non", "oui")
        ):
            reactions = ["✅", "❌"]
        else:
            reactions = [
                "1️⃣",
                "2️⃣",
                "3️⃣",
                "4️⃣",
                "5️⃣",
                "6️⃣",
                "7️⃣",
                "8️⃣",
                "9️⃣",
                "🔟",
            ]

        description = []
        for x, option in enumerate(options):
            description += "\n {} {}".format(reactions[x], option)
        question += "\nPlusieurs votes par personne ? "
        question += "oui" if multivote else "non"
        embed = discord.Embed(title=question, description="".join(description))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[: len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text="Poll ID: {}".format(react_message.id))
        await react_message.edit_message(embed=embed)

    @commands.hybrid_command(
        name="tally",
        description="Compte les votes d'un sondage",
    )
    async def tally(self, ctx, id=None):
        poll_message = await ctx.channel.fetch_message(id)
        user_can_multivote = poll_message.embeds[0].title[-3:] == "oui"
        print(user_can_multivote)
        embed = poll_message.embeds[0]

        # On retire la dernière phrase, qui fait 36 caractères
        title = embed.title[:-36]

        splitted_description = embed.description.split("\n")
        splitted_description = [x.strip() for x in splitted_description]
        if splitted_description[0][:3] == "1️⃣":
            # Liste à nombre
            opt_dict = {
                reaction[:3]: reaction[3:].strip()
                for reaction in splitted_description[:9]
            }
            if len(splitted_description) == 10:
                # If there is a tenth option, split it differently (because it works that way 🤷)
                opt_dict["🔟"] = splitted_description[9][2:].strip()
        else:
            # yes/no
            opt_dict = {
                reaction[:1]: reaction[2:].strip()
                for reaction in splitted_description
            }

        voters = [
            self.bot.user.id
        ]  # add the bot's ID to the list of voters to exclude it's votes

        tally = {x: 0 for x in opt_dict.keys()}
        for reaction in poll_message.reactions:
            if reaction.emoji in opt_dict.keys():
                reactors = [user async for user in reaction.users()]
                for reactor in reactors:
                    if reactor.id not in voters:
                        tally[reaction.emoji] += 1
                        if not user_can_multivote:
                            voters.append(reactor.id)
        output = f"Results of the poll for '{title}':\n" + "\n".join(
            [
                "{}: {}".format(opt_dict[key], tally[key])
                for key in tally.keys()
            ]
        )
        await ctx.channel.send(output)


async def setup(bot) -> None:
    manager = ForumManager(bot)
    await bot.add_cog(manager)
    await manager.reload()
