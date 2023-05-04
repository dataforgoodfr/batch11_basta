import os
from dotenv import load_dotenv
from json import load
from datetime import timezone, time

__all__ = ["COMMON_MESSAGES",
"BOT_TOKEN",
"RAW_CONFIGURATION",
"CHAT_SCRIPT",
"OPENING_CHANNEL_HOUR_TIMES",
"CLOSING_CHANNEL_HOUR_TIMES",
"MESSAGE_HOUR_TIMES",
"SCRIPT_DAY_LENGTH"
]

load_dotenv()
utc = timezone.utc


with open("scripts/common_messages.json") as json_data_file:
    COMMON_MESSAGES = load(json_data_file)


with open("configuration.json") as json_data_file:
    RAW_CONFIGURATION = load(json_data_file)

with open("scripts/discuss_script.json") as json_data_file:
    CHAT_SCRIPT = load(json_data_file)

BOT_TOKEN = os.getenv("BOT_TOKEN")

OPENING_CHANNEL_HOUR_TIMES = [time(hour=RAW_CONFIGURATION["OPENING_CHANNEL_HOUR"], tzinfo=utc)]

CLOSING_CHANNEL_HOUR_TIMES = [time(hour=RAW_CONFIGURATION["CLOSING_CHANNEL_HOUR"], tzinfo=utc)]

MESSAGE_HOUR_TIMES = [
    time(hour=RAW_CONFIGURATION["FIRST_MESSAGE_HOUR"], tzinfo=utc),
    time(hour=RAW_CONFIGURATION["SECOND_MESSAGE_HOUR"], tzinfo=utc),
    time(hour=RAW_CONFIGURATION["THIRD_MESSAGE_HOUR"], tzinfo=utc),
]

SCRIPT_DAY_LENGTH = int(RAW_CONFIGURATION["SCRIPT_DAY_LENGTH"])

