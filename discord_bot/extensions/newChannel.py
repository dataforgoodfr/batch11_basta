from discord.ext import commands, tasks

@client.command()
@dataclass
class CreateChannel():
    
    async def create_channel(self, *, name=None):
        guild = self.message.guild
        if name is None:
            await self.send('Sorry, but you have to insert a name. Try again, but do it like this: `>create [channel name]`')
        else:
            await guild.create_text_channel(name)
            await self.send(f"Created a channel named {name}")