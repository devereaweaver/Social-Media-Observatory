import configparser
import os 
import platform

# Point to the config file
HOME_DIR = (
    os.environ["USERPROFILE"] if platform.system() == "Windows"
    else os.environ["HOME"]
)
config_file_full_path = os.path.join(HOME_DIR, "smo_config.cfg")

# Instantiate a config manager object
config = configparser.ConfigParser()

# Read in the config file
config.read(config_file_full_path)

# Extract the config data into Python variables (optional)
app_name=config['telegram-credentials']['app-name']
api_id=config['telegram-credentials']['api-id']
api_hash=config['telegram-credentials']['api-hash']