from ch2.backend.get_channel_info import run
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description="This script retrieves Telegram channel metada.")
parser.add_argument(
    "--credentials",
    help="The credentials to use for the Telegram API.",
    default="telegram-credentials",
)

args = parser.parse_args()

print(f"Using credentials: {args.credentials} for credentials...")
run(args.credentials)