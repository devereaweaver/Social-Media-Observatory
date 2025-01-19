# Proof of concept to prove we can retrieve channel metadata from the Telegram API

from telethon.sync import TelegramClient
from telethon import functions

# Configuration data
app_name =  "D's SMOP"
api_id = 27996747
api_hash = "6cfd4e4453cb1b91d8c5590d9d20c6f0"

# Input data
channel_names = ["rybar", "mig41"]

# Retrieve channel metadata from Telegram API
with TelegramClient(app_name, api_id, api_hash) as client:
    for channel_name in channel_names:
        channel_object = client(functions.channels.GetFullChannelRequest(channel=channel_name))

    if channel_object is not None:
        print(channel_object.to_dict())