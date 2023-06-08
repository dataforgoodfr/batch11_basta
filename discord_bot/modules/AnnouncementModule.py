"""
    Ce module doit servir à envoyer des messages tout au long de la journée
    Il sera invoqué par le scheduler du forum
"""

import json
import logging

# Open script.json and load script
with open("script.json") as script_file:
    SCRIPT = json.load(script_file)


async def send_already_started_message(ctx, bot):
    await ctx.channel.send("Le forum a déjà commencé !")


async def send_start_of_forum_message(ctx, bot):
    channel = ctx.channel
    await channel.send("Début du forum")


# Envoye le message suivant sur le bon channel
async def send_next_message(config: dict, bot) -> dict:
    current_day = config["GENERAL"]["CURRENT_DAY"]
    current_question = config["GENERAL"]["CHANNELS"]["DAYS"][current_day][
        "QUESTION_NO"
    ]

    # Next question
    current_question += 1

    if current_day == -1:
        logging.error("Le forum n'est pas encore lancé.")
    else:
        # If there is no more message to send
        if current_question >= len(SCRIPT[f"day{current_day}"]["script"]):
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
            channel = bot.get_channel(channel_id)
            day_script = SCRIPT[f"day{current_day}"]["script"][
                current_question
            ]
            await channel.send(day_script)

        # Update the config
        config["GENERAL"]["CHANNELS"]["DAYS"][current_day][
            "QUESTION_NO"
        ] = current_question

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
    await channel.send(f"Fin de la journée n°{current_day+1}")


async def send_end_of_forum_message(days_config: dict, bot):
    # Send the end of forum message
    channel_id = days_config[-1]["CHANNEL_ID"]
    if channel_id == -1:
        logging.error(
            f"Le channel id du jour {len(days_config)} n'est pas défini."
        )
    channel = bot.get_channel(channel_id)
    await channel.send("Fin du forum")


async def send_opening_messages(channelsIds: list[int], bot) -> None:
    for channel_id in channelsIds:
        channel = bot.get_channel(channel_id)
        await channel.send("Vous pouvez de nouveau écrire dans ce channel.")


async def send_closing_messages(channelsIds: list[int], bot) -> None:
    for channel_id in channelsIds:
        channel = bot.get_channel(channel_id)
        await channel.send("Vous ne pouvez plus écrire dans ce channel.")
