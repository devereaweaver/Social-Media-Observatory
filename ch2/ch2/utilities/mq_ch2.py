#  Message queue script that defines the functions to send messages to the jobs queue
import pika   # not needed if keeping version as is, if using, change code in get_channel_info.py
from ..config import pikaparams
import json

def get_channel():
    connection = pika.BlockingConnection(pikaparams)
    channel = connection.channel()
    return channel

def send_data_to_queue(messages: list[dict], target_queue: str):
    """
    Send data to the message queue to be processed by the backend.
    """
    channel = get_channel()
    channel.queue_declare(queue=target_queue, durable=True)

    # Send messages 
    for message in messages:
        channel.basic_publish(   # push message to queue as byte-encoded dict
            exchange="",
            routing_key=target_queue,
            body=json.dumps(message).encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),  # make message persistent
        )
    print("Data sent to queue!")