# This example requires the 'message_content' intent.

import discord

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    print(
        f"{message.channel}: {message.author}: {message.author.name}: {message.content}"
    )

    if message.author == client.user:  # Won't track its own messages
        return

    if message.content.lower().startswith("hello"):
        await message.channel.send("Hello!")


if BOT_TOKEN:
    client.run(BOT_TOKEN)
