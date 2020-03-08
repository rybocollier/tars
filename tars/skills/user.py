from slackclient import SlackClient
import sys

def get_user_id(event_data):
    ''' Return user's ID '''
    user_id = event_data["event"]["user"]
    return user_id 

def get_user_name(slack_client, SLACK_TOKEN, user_id):
    ''' Return user's name '''
    user_data = slack_client.api_call(
        "users.info",
        token=SLACK_TOKEN,
        user=user_id,
    )
    return user_data["user"]["name"]
