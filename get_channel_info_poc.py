# Proof of concept to prove we can retrieve channel metadata from the Telegram API
# Note: This POC code is a sequential version, may consider using async version for production


from telethon.sync import TelegramClient
from telethon import functions

# Input data
channel_names = ["rybar", "mig41"]

# Retrieve channel metadata from Telegram API
with TelegramClient(app_name, api_id, api_hash) as client:
    for channel_name in channel_names:
        channel_object = client(functions.channels.GetFullChannelRequest(channel=channel_name))

    if channel_object is not None:
        print(channel_object.to_dict())
    