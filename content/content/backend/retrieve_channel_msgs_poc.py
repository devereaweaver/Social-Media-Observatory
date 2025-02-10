# Given a Telegram handle. retrieve some of its messages using the Telegram API.
# This is only a POC script.
from telethon import TelegramClient
import configparser
import os
from ..config import *

def run():
    # Point to config file 
    HOME_DIR = os.environ["USERPROFILE"] if platform.system() == "Windows" else os.environ["HOME"]
    config_file_full_path = os.path.join(HOME_DIR, "smo_config.cfg")
    config = configparser.ConfigParser()
    config.read(config_file_full_path)

    app_name = config['telegram-credentials']['app-name']
    api_id = config['telegram-credentials']['api-id']
    api_hash = config['telegram-credentials']['api-hash']

    channel_name = "rybar"

    # Retrieve messages 
    with TelegramClient(app_name, api_id, api_hash) as client:
        # iter_messages() queries the API endpoint for a given channel's messages, 
        # setting max_id = min_id = 0 will impose now upper bound on messages, it will
        # simply return them in reverse-chronological order
        message_batch = client.iter_messages(channel_name, min_id=0, max_id=0, limit=100)

        # print messages
        for message in message_batch:
            print(message.to_dict())