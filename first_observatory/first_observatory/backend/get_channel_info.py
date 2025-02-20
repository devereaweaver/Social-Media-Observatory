# Event-driven version of get_channel_info_poc.py which will start the process in the backend
# that will run in perpetuity while listening for jobs from investigators via the frontend.
# POC script to get channel metadata from Telegram API. 
# Script has been modified to consume messages from a RabbitMQ queue. 

import json
from ..config import *
from ..utilities.logic_ch2 import retrieve_and_save_channel_metadata
from ..utilities.mq_ch2 import get_channel


def consumer(app_name, api_id, api_hash):
    """
    Listen for messages from the message queue and process them. When aa message is received,
    execute the callback function to process the message, execute the task, and acknowledge the job
    is completed.
    """

    def callback(ch, method, properties, body):
        # Receive and parse message
        message = json.loads(body.decode("utf-8"))  # decode json message
        channel_names = message["handles"]  # extract channel names from message
        seed_list_name = message["seed_list"]  # extract seed list name from message

        # Call retrieve_and_save_channel_metadata function to get channel metadata
        # This is the function that will process the data.
        retrieve_and_save_channel_metadata(
            channel_names, app_name, api_id, api_hash, seed_list_name
        )

        # Contact queue to acknowledge the message has been received and processed
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("task complete!")

    input_channel = get_channel()
    input_channel.queue_declare(queue=handles_queue, durable=True)
    input_channel.basic_qos(prefetch_count=1)
    input_channel.basic_consume(on_message_callback=callback, queue=handles_queue)
    print("listening for handles to look up...")
    input_channel.start_consuming()


def run(args_credentials):
    """
    Execute consumer function to listne for messages from the message queue and process them
    in perpetuity.
    """
    consumer(
        config[args_credentials]["app-name"],
        config[args_credentials]["api-id"],
        config[args_credentials]["api-hash"],
    )