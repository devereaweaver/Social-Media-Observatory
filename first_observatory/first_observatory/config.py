# config.py - load config data from file in user's home directory
import configparser
import os 
import platform
import pika

# Point to config file 
HOME_DIR = os.environ["USERPROFILE"] if platform.system() == "Windows" else os.environ["HOME"]

config_file_full_path = os.path.join(HOME_DIR, "smo_config.cfg")

# Instantiate config manager object
config = configparser.ConfigParser()

# Load config data from file
config.read(config_file_full_path)

# Extract config data into Python variables (optional)
app_name = config['telegram-credentials']['app-name']
api_id = config['telegram-credentials']['api-id']
api_hash = config['telegram-credentials']['api-hash']

pikaparams = pika.ConnectionParameters(
    config["rabbit-mq"]["host"],
    credentials=pika.PlainCredentials(
        config["rabbit-mq"]["user"],
        config["rabbit-mq"]["password"]
    ),
    heartbeat=int(config["rabbit-mq"]["heartbeat"]),
    blocked_connection_timeout=int(config["rabbit-mq"]["blocked-connection-timeout"]),
)

handles_queue = config["rabbit-mq"]["telegram-handles-queue"]
channel_metadata_table_name = config["telegram-db"]["channel-metadata-table"]
#seed_table_name = config["telegram-db"]["channel-seed-table"]