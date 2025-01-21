def extract_data_dictionary_from_channel_object(channel_object):
    """
    Telegram API returns a channel object in JSON format. This function extracts the
    relevant data from the channel object into the table columns we're interested in.
    We will also keep the entire original JSON object in the api_response column for
    analysis and legal purposes.
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
