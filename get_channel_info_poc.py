# Proof of concept to prove we can retrieve channel metadata from the Telegram API
# Note: This POC code is a sequential version, may consider using async version for production

from telethon.sync import TelegramClient
from telethon import functions
from config import app_name, api_id, api_hash
from database_connect_ch2 import insert_data_into_channel_metadata_table
from logic import extract_data_dictionary_from_channel_object

# Input data
channel_names = ["rybar", "mig41"]
#channel_names = ["rybar"]


# Running list of records
records = []

# Retrieve channel metadata from Telegram API
with TelegramClient(app_name, api_id, api_hash) as client:
    for channel_name in channel_names:
        channel_object = client(functions.channels.GetFullChannelRequest(channel=channel_name))

        # Store non-empty returned objects in records list and extract relevant fields 
        # to Postgres table columns
        if channel_object is not None:
            records.append(extract_data_dictionary_from_channel_object(channel_object))

# Insert the data into our Postgres table
if len(records) > 0:
    insert_data_into_channel_metadata_table(records) # pass list of records to function
    print("Data inserted successfully")
else:
    print("Error: Insertion failed")