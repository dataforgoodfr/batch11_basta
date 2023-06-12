import logging
import logging.handlers
import os


def setupLogger():
    # If logs folder doesn't exist, create it
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # get root logger
    logger = logging.getLogger()

    # format log messages
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

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
    logging_file_name = "logs/discord.log"
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=logging_file_name,
        when="midnight",
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    logger.addHandler(file_handler)

    logger.setLevel(logging.INFO)
