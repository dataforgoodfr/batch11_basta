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

    # TODO :
    # - Faire le système qui fait des stats
    
    async def get_tools(self) -> None:
        return self.bot.get_cog("Tools")

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        # ATTENTION, il recoit ses propres messages

        if message.author != self.bot.user and not message.content.startswith(
            ("!", "/", ".")
        ):
            self.messages.append(message)

    async def make_daily_conclusion(self, dayNb : int) -> None:
        logging.debug("Making daily conclusion")

        tools = await self.get_tools()

        # Envoyer un message de fin de journée
        # # Remerciements
        # # Récapitulatif de l'engagement sur la journée
        # # Annonce des thèmes de la journée suivante
        # # Rappel des règles et des contacts

        
        await tools.send_message(dataImport.COMMON_MESSAGES['endDayThanks'])

        # Récapitulatif de l'engagement sur la journée
        phrase = "Le prochain theme est : " + dataImport.CHAT_SCRIPT['day'+str(dayNb)]['theme']
        await tools.send_message(phrase)

        # Rappel des règles
        await tools.send_message(dataImport.COMMON_MESSAGES['reglesRappel'])
        await tools.send_message(dataImport.COMMON_MESSAGES['contactRappel'])

    async def make_final_conclusion(self) -> None:
        logging.debug("Making final conclusion")



# Adding the cog to the bot. It is required to do this in order to use the commands
async def setup(bot) -> None:
    await bot.add_cog(ConclusionGenerator(bot))
