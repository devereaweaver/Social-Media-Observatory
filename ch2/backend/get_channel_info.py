# Event-driven version of get_channel_info_poc.py which will start the process in the backend
# that will run in perpetuity while listening for jobs from investigators via the frontend.
# POC script to get channel metadata from Telegram API. 
# Script has been modified to consume messages from a RabbitMQ queue. 

# TODO: Need to change the directory structure to match the import statements
# and implement the functions that are imported below.
import json
from ..config import *
from ..utilities.logic_ch2 import retrieve_and_save_channel_metadata
from ..utitliies.mq_ch2 import get_channel


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
        ch.back_ack(delivery_tag=method.delivery_tag)
        print("task complete!")

        # TODO: Implement the pikaparams for this to actually work, they'll be defined in the
        # configuration file in the home directory
        # Also need to implement configuration for handles_queue
        connection = pika.BlockingConnection(pikaparams)
        input_channel = connection.channel()
        input_channel.queue_declare(queue=handles_queue, durable=True)
        input_channel.basic_qos(prefetch_count=1)
        input_channel.basic_consume(queue=handles_queue, on_message_callback=callback)
        print("listening for handles to look up...")
        input_channel.start_consuming()


# Execute consumer function
consumer(
    config["telegram-credentials"]["app-name"],
    config["telegram-credentials"]["api-id"],
    config["telegram-credentials"]["api-hash"],
)
