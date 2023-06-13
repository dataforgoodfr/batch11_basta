"""
Module qui servira à faire les rapports en fin de journée ou de forum
"""
import logging
import os


async def generate_daily_report(forum) -> None:
    logging.info("Generating daily report...")
    logging.info("Done!")


async def generate_forum_report(forum) -> None:
    logging.info("Generating forum report...")

    logging.info("Fecthing all messages")

    # get guild from guild id
    guild = forum.bot.get_guild(forum.server_id)

    # get all channels
    channels = guild.text_channels

    # If there are channel we're not supposed to log, remove them
    not_log_channels = forum.get_data("not_log_channels")
    if type(not_log_channels) is list:
        channels = [
            channel
            for channel in channels
            if channel.id not in not_log_channels
        ]

    # fetch all messages
    messages = []
    for channel in channels:
        channel_messages = [
            message async for message in channel.history(limit=None)
        ]
        messages.extend(channel_messages)

    # sort messages by date
    messages.sort(key=lambda x: x.created_at)

    file_name = "messages_report.txt"

    # if the report folder doesn't exist, create it
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # write messages in a file
    with open(f"reports/{file_name}", "w", encoding="utf-8") as f:
        for message in messages:
            try:
                # write in utf-8
                f.write(f"{message.author.name} : {message.content}\n")
            except Exception as e:
                logging.error(
                    f"Error while writing message {message.id} : {e}"
                )
                continue

    logging.info("Forum report done!")
