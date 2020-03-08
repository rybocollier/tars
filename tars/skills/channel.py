from slackclient import SlackClient

def get_channel_id(event_data):
    ''' Return channel ID '''
    channel_id = event_data["event"]["channel"]
    return channel_id 

def get_channel_name(slack_client, SLACK_TOKEN, channel_id):
    ''' Return channel name '''
    channel_name = slack_client.api_call(
        "channels.info",
        token=SLACK_TOKEN,
        channel=channel_id,
    )
    return channel_name
