# POC script to get channel metadata from Telegram API 
from telethon.sync import TelegramClient
from telethon import functions
from config import app_name, api_id, api_hash

# Hardcode input data
channel_names = ["rybar", "mig41"]

# Retrieve channel metadata 
with TelegramClient(app_name, api_id, api_hash) as client:
    for channel_name in channel_names:
        channel_object = client(functions.channels.GetFullChannelRequest(channel=channel_name))
    
    if channel_object is not None:
        print(channel_object.to_dict())