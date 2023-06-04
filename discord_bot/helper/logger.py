import logging
import os
from datetime import datetime


def setupLogger():
    # If logs folder doesn't exist, create it
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # get root logger
    logger = logging.getLogger()

    # Add stream handler (the console)
    logger.addHandler(logging.StreamHandler())

    # Add file handler
    logging_file_name = (
        f"logs/{datetime.now().strftime('discord%Y-%m-%d-%H-%M-%S.log')}"
    )
    logger.addHandler(
        logging.FileHandler(
            filename=logging_file_name, encoding="utf-8", mode="w"
        )
    )

    # set logging level
    logger.setLevel(logging.DEBUG)

    # TODO
    # - Add a formatter to the file handler
    # - Add a different log level for file than for stream:
    #   - stream must be warning
    #   - file must be debug
    # - Add a rotating file handler
