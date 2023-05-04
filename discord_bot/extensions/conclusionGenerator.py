from discord.ext import commands
from discord import Message

from dataclasses import dataclass, field

import logging

import helpers.constantsImport as dataImport

__all__ = ["ConclusionGenerator"]



@dataclass
class ConclusionGenerator(commands.Cog):
    bot: commands.Bot
    messages: list[Message] = field(default_factory=list)  # Store the messages

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        # ATTENTION, il recoit ses propres messages

        if message.author != self.bot.user and not message.content.startswith(
            ("!", "/", ".")
        ):
            self.messages.append(message)

    async def make_daily_conclusion(dayNb : int) -> None:
        logging.debug("Making daily conclusion")

        # Envoyer un message de fin de journée
        # # Remerciements
        # # Récapitulatif de l'engagement sur la journée
        # # Annonce des thèmes de la journée suivante
        # # Rappel des règles et des contacts

        # dataImport.COMMON_MESSAGES.endDayThanks
        
        # Faire un fichier helper qui fait tous les imports et qu'on aura juste à appeler avec dataImport.[constante]
        # Faire un fichier helper qui fait des fonctions utiles comme "envoyer un message sur le canal classique"

        

    async def make_final_conclusion(self) -> None:
        logging.debug("Making final conclusion")


# Adding the cog to the bot. It is required to do this in order to use the commands
async def setup(bot) -> None:
    await bot.add_cog(ConclusionGenerator(bot))
