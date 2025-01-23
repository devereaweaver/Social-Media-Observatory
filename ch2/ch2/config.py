# config.py - load config data from file in user's home directory
import configparser
import os 
import platform

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