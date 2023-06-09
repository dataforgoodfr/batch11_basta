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

    save_poll(forum, react_message.id)


# async def get_polls_result(ctx, forum, bot):
#     poll_message = await ctx.channel.fetch_message(id)
#     user_can_multivote = poll_message.embeds[0].title[-3:] == "oui"
#     embed = poll_message.embeds[0]

#     # On retire la dernière phrase, qui fait 36 caractères
#     title = embed.title[:-36]

#     splitted_description = embed.description.split("\n")
#     splitted_description = [x.strip() for x in splitted_description]
#     if splitted_description[0][:3] == "1️⃣":
#         # Liste à nombre
#         opt_dict = {
#             reaction[:3]: reaction[3:].strip()
#             for reaction in splitted_description[:9]
#         }
#         if len(splitted_description) == 10:
#             # If there is a tenth option, split it differently
#             # (because it works that way 🤷)
#             opt_dict["🔟"] = splitted_description[9][2:].strip()
#     else:
#         # yes/no
#         opt_dict = {
#             reaction[:1]: reaction[2:].strip()
#             for reaction in splitted_description
#         }

#     voters = [
#         bot.user.id
#     ]  # add the bot's ID to the list of voters to exclude it's votes

#     tally = {x: 0 for x in opt_dict.keys()}
#     for reaction in poll_message.reactions:
#         if reaction.emoji in opt_dict.keys():
#             reactors = [user async for user in reaction.users()]
#             for reactor in reactors:
#                 if reactor.id not in voters:
#                     tally[reaction.emoji] += 1
#                     if not user_can_multivote:
#                         voters.append(reactor.id)
#     output = f"Results of the poll for '{title}':\n" + "\n".join(
#         ["{}: {}".format(opt_dict[key], tally[key]) for key in tally.keys()]
#     )
#     await ctx.channel.send(output)


def save_poll(forum, pollId: int) -> None:
    polls_data = forum.get_data("polls")
    if polls_data == {}:
        polls_data = [pollId]
    else:
        polls_data.append(pollId)
    forum.save_data("polls", polls_data)
