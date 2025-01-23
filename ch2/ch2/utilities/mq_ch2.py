#  Message queue script that defines the functions to send messages to the jobs queue
import pika   # not needed if keeping version as is, if using, change code in get_channel_info.py
from ..config import pikaparams
import json

def get_channel():
    connection = pika.BlockingConnection(pikaparams)
    channel = connection.channel()
    return channel

def send_data_to_queue(messages: list[dict], target_queue: str):
    pass