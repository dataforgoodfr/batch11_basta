"""
    Ce module doit servir à envoyer des messages tout au long de la journée
    Il sera invoqué par le scheduler du forum
"""

import json

# Open script.json and load script
with open("script.json") as script_file:
    SCRIPT = json.load(script_file)


# Envoye le message suivant sur le bon channel
async def send_next_message(days_config: dict, bot) -> dict:
    current_day, current_question = get_current_state(days_config)

    # Next question
    current_question += 1

    # If there is no more message to send
    if current_question == len(SCRIPT[f"day{current_day}"]):
        print("No more message to send")
    else:
        # Send the message

        channel_id = days_config[current_day]["CHANNEL_ID"]
        if channel_id == -1:
            raise ValueError(
                "The channel id is not set in the config. Please set it."
            )
        channel = bot.get_channel(channel_id)
        day_script = SCRIPT[f"day{current_day}"]["script"][current_question]
        await channel.send(day_script)

    # Update the config
    days_config[current_day]["QUESTION_NO"] = current_question

    return days_config


# return the day and the last question asked in a tuple
def get_current_state(days_config: dict) -> tuple:
    day_nb = -1
    last_question = -1

    # Will stop when it will find a day with no questions
    for i in range(len(days_config)):
        if days_config[i]["IS_CURRENT_DAY"]:
            day_nb = i
            last_question = days_config[day_nb]["QUESTION_NO"]
            break

    return (day_nb, last_question)
