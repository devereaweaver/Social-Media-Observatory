# Publish messages to the jobs queue 

from ..config import handles_queue
from ..utilities.mq_ch2 import send_data_to_queue

# Key-value pairs to be sent to the message queue
# TODO: Why are hardcoding the handles here?
# Hypotheitical message w/requisite handles and seed list
message = {
    "handles": ["rybar", "mig41"], 
    "seed_list": "russian_disinfo"
    }

def run():
    """
    Calls function to send out data to the jobs queue 
    for the backend to process. The function takes a list of 
    # key-value pairs representing a message and a string to identify the queue
    we want to send the message to.
    """
    send_data_to_queue([message], handles_queue)

if __name__ == "__main__":
    run()