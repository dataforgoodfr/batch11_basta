import logging
import os
from datetime import datetime


def setupLogger():
    # If logs folder doesn't exist, create it
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # get root logger
    logger = logging.getLogger()

    # format log messages
    formatter = logging.Formatter('%(levelname)s:%(message)s')

    # logging level
    level = logging.INFO
    logger.setLevel(logging.INFO)

    # Add stream handler (the console)
    # Déjà récupéré par un autre moyen
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)
    # console_handler.setLevel(level)

    # logger.addHandler(console_handler)

    # Add file handler
    logging_file_name = (
        f"logs/{datetime.now().strftime('discord%Y-%m-%d-%H-%M-%S.log')}"
    )
    file_handler = logging.FileHandler(
            filename=logging_file_name, encoding="utf-8", mode="w"
        )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    logger.addHandler(file_handler)
