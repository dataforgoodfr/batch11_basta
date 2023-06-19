"""
    Ce module doit servir à envoyer des messages tout au long de la journée
    Il sera invoqué par le scheduler du forum
"""

import json
import logging

import modules.PollModule as PollModule

# Open script.json and load script
with open("script/script.json", encoding="utf-8") as script_file:
    SCRIPT = json.load(script_file)


async def send_already_started_message(ctx, bot):
    await ctx.channel.send("Le forum a déjà commencé !")


async def send_start_of_forum_message(ctx, bot):
    channel = ctx.channel
    await channel.send("Lancement du forum, bienvenues à toutes !")


# Envoye le message suivant sur le bon channel
async def send_next_message(bot, forum) -> dict:
    config = forum.config
    current_day = config["GENERAL"]["CURRENT_DAY"]
    message_no = config["GENERAL"]["CHANNELS"]["DAYS"][current_day][
        "QUESTION_NO"
    ]

    # Next question
    message_no += 1

    if current_day == -1:
        logging.error("Le forum n'est pas encore lancé.")
    else:
        # If there is no more message to send
        if message_no >= len(SCRIPT[current_day]):
            logging.warn("No more message to send")
        else:
            # Send the message
            channel_id = config["GENERAL"]["CHANNELS"]["DAYS"][current_day][
                "CHANNEL_ID"
            ]
            if channel_id == -1:
                logging.error(
                    f"Le channel id du jour {current_day} n'est pas défini."
                )

            day_script = SCRIPT[current_day]
            day_send = day_script[message_no]
            to_send_message = day_send["message"]
            to_send_polls = day_send["polls"]
            channel = bot.get_channel(channel_id)
            if to_send_message != "":
                if day_send["ping"]:
                    role_to_ping = config["ROLE_MANAGER"]["BASE_ROLE_ID"]
                    to_send_message = f"{to_send_message}\n<@&{role_to_ping}>"
                await channel.send(to_send_message)
            await PollModule.send_polls(to_send_polls, channel, forum)

        # Update the config
        config["GENERAL"]["CHANNELS"]["DAYS"][current_day][
            "QUESTION_NO"
        ] = message_no

        return config


async def send_end_of_day_message(config: dict, bot):
    current_day = config["GENERAL"]["CURRENT_DAY"]

    # Send the end of day message
    channel_id = config["GENERAL"]["CHANNELS"]["DAYS"][current_day][
        "CHANNEL_ID"
    ]
    if channel_id == -1:
        logging.error(f"Le channel id du jour {current_day} n'est pas défini.")
    channel = bot.get_channel(channel_id)
    if current_day <= 3:
        await channel.send(
            f"Fin de la journée n°{current_day+1}, merci d'avoir participé \
et à demain."
        )


async def send_end_of_forum_message(config: dict, bot):
    # Send the end of forum message
    channel_id = config["GENERAL"]["CHANNELS"]["DAYS"][-1]["CHANNEL_ID"]
    current_day = config["GENERAL"]["CURRENT_DAY"]
    if channel_id == -1:
        logging.error(f"Le channel id du jour {current_day} n'est pas défini.")
    channel = bot.get_channel(channel_id)
    await channel.send("Fin du forum, merci à toutes d'avoir participé !")


async def send_opening_messages(channelsIds: list[int], bot) -> None:
    for channel_id in channelsIds:
        channel = bot.get_channel(channel_id)
        await channel.send(
            "Début de journée, tu peux de nouveau écrire dans ce channel."
        )


async def send_closing_messages(channelsIds: list[int], bot) -> None:
    for channel_id in channelsIds:
        channel = bot.get_channel(channel_id)
        await channel.send(
            "Fin de journée, tu ne peux plus écrire \
dans ce channel jusqu'à demain."
        )
