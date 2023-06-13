"""
    Ce module sert à créer et gérer les sondages
"""

import logging

import discord


async def send_polls(polls, channel, forum) -> None:
    _ = [await send_poll(poll, channel, forum) for poll in polls]


async def send_poll(poll: dict, channel, forum) -> int:
    question: str = poll["question"]
    options: list[str] = poll["options"]
    multivote: bool = poll["multivote"]

    if len(options) <= 1:
        logging.warn("Cannot send poll : need at least 2 options")
        if channel:
            await channel.send("You need more than one option to make a poll!")
        return
    if len(options) > 10:
        logging.warn("Cannot send poll : need at more 10 options")
        if channel:
            await channel.send(
                "You cannot make a poll for more than 10 things!"
            )
        return
    if len(options) == 2 and (
        (options[0].lower(), options[1].lower()) == ("oui", "non")
        or (options[0].lower(), options[1].lower()) == ("non", "oui")
    ):
        reactions = ["✅", "❌"] if options[0].lower() == "oui" else ["❌", "✅"]
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

    # Ajout d'une phrase pour préciser le type du multivote
    description = []
    for x, option in enumerate(options):
        description += "\n {} {}".format(reactions[x], option)
    if multivote:
        question += "\nVous pouvez voter pour plusieurs options."
    else:
        question += "\nVous ne devez voter que pour une seule option."

    # Formatage de l'embed
    embed = discord.Embed(title=question, description="".join(description))
    react_message = await channel.send(embed=embed)
    for reaction in reactions[: len(options)]:
        await react_message.add_reaction(reaction)
    embed.set_footer(text="Poll ID: {}".format(react_message.id))

    await react_message.edit(embed=embed)

    save_poll(forum, react_message)


async def fetch_polls(forum) -> None:
    data_polls = forum.get_data("polls")
    if type(data_polls) is dict:
        bot = forum.bot

        polls = []

        for message_id, channel_id in data_polls.items():
            # get the message object from the channel
            channel = bot.get_channel(channel_id)
            poll_message = await channel.fetch_message(message_id)

            embed = poll_message.embeds[0]

            # On retire la dernière phrase du titre
            title = "\n".join(embed.title.split("\n")[:-1])

            splitted_description = embed.description.split("\n")
            splitted_description = [x.strip() for x in splitted_description]
            if splitted_description[0][:3] == "1️⃣":
                # Liste à nombre
                opt_dict = {
                    reaction[:3]: reaction[3:].strip()
                    for reaction in splitted_description[:9]
                }
                if len(splitted_description) == 10:
                    # If there is a tenth option, split it differently
                    # (because it works that way 🤷)
                    opt_dict["🔟"] = splitted_description[9][2:].strip()
            else:
                # yes/no
                opt_dict = {
                    reaction[:1]: reaction[2:].strip()
                    for reaction in splitted_description
                }

            voters = [
                bot.user.id
            ]  # add the bot's ID to the list of voters to exclude it's votes

            tally = {x: 0 for x in opt_dict.keys()}
            for reaction in poll_message.reactions:
                if reaction.emoji in opt_dict.keys():
                    reactors = [user async for user in reaction.users()]
                    for reactor in reactors:
                        if reactor.id not in voters:
                            tally[reaction.emoji] += 1

            poll = {
                "title": title,
                "description": embed.description,
                "tally": tally,
                "opt_dict": opt_dict,
            }
            polls.append(poll)

            output = f"Results of the poll for '{title}':\n" + "\n".join(
                [
                    "{}: {}".format(opt_dict[key], tally[key])
                    for key in tally.keys()
                ]
            )
            logging.info("Logged poll results :\n" + output)
        forum.save_data("poll_results", polls)


def save_poll(forum, message) -> None:
    """
    Structure de données d'un sondage
    {
        messageId:channelId
    }
    """
    polls_data = forum.get_data("polls")
    if type(polls_data) is dict:
        polls_data[message.id] = message.channel.id
    else:
        polls_data = {message.id: message.channel.id}
    forum.save_data("polls", polls_data)


def is_multivote_allowed(reaction) -> bool:
    title = reaction.message.embeds[0].title
    return "\nVous pouvez voter pour plusieurs options." in title


def is_poll(forum, reaction) -> bool:
    data_polls = forum.get_data("polls")
    if type(data_polls) is not dict:
        return False
    else:
        return reaction.message.id in data_polls.keys()


async def checkReaction(user_reaction, user, forum):
    if is_poll(forum, user_reaction) and not user.bot:
        if not is_multivote_allowed(user_reaction):
            # On retire les autres réactions
            for reaction in user_reaction.message.reactions:
                if reaction.emoji != user_reaction.emoji:
                    await reaction.remove(user)
