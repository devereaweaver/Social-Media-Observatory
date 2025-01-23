# logic_ch2.py - contains helper functions


def extract_data_dictionary_from_channel_object(channel_object):
    """
    Takes an API response object parses it to extract the relevant data to be
    stored in the relevant colums in the database table.
    Returns a dictionary with the extracted data (key-value pairs) that will
    be inserted into the database table.
    """
    return {
        "channel_name": channel_object.to_dict()["chats"][0]["username"],
        "channel_id": channel_object.to_dict()["full_chat"]["id"],
        "channel_title": channel_object.to_dict()["chats"][0]["title"],
        "num_subscribers": channel_object.to_dict()["full_chat"]["participants_count"],
        "channel_bio": channel_object.to_dict()["full_chat"]["about"],
        "channel_birthdate": channel_object.to_dict()["chats"][0]["date"],
        "api_response": channel_object.to_json(),
    }
