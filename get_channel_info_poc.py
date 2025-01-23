# POC script to get channel metadata from Telegram API
from telethon.sync import TelegramClient
from telethon import functions
from config import app_name, api_id, api_hash
from db_ch2 import insert_data_into_channel_metadata_table
from logic_ch2 import extract_data_dictionary_from_channel_object

# Hardcode input data
channel_names = ["rybar", "mig41"]

# Empty list to store records pulled from API 
records = []

# Retrieve channel metadata
with TelegramClient(app_name, api_id, api_hash) as client:
    for channel_name in channel_names:
        channel_object = client(
            functions.channels.GetFullChannelRequest(channel=channel_name)
        )

        # Extract interesting data from returned API object into format
        # that matches the database schema, then add each one to the records list
        if channel_object is not None:
            records.append(extract_data_dictionary_from_channel_object(channel_object))

# Store data into table
if len(records) > 0:
    insert_data_into_channel_metadata_table(records)