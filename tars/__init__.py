import os
import sys
import time
from flask import Flask, request, Response
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter

# import tars skills
from tars.skills.user import get_user_id, get_user_name
from tars.skills.channel import get_channel_id, get_channel_name

# instantiate flask app
app = Flask(__name__)

# import environment variables
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET', None)

# instantiate slack client
slack_client = SlackClient(SLACK_TOKEN)

def print_debug(input):
    print(input, file=sys.stderr)

slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
  emoji = event_data["event"]["reaction"]
  print_debug(emoji)

@slack_events_adapter.on("member_joined_channel")
def member_joined(event_data):
    # match user ID to user name
    user_name = get_user_name(slack_client, SLACK_TOKEN, get_user_id(event_data))
    message = "Hello " + user_name + "." 
    slack_client.api_call("chat.postMessage", channel=get_channel_id(event_data), text=message)

@slack_events_adapter.on("member_left_channel")
def member_left(event_data):
    # match user ID to user name
    user_name = get_user_name(slack_client, SLACK_TOKEN, get_user_id(event_data))
    message = "See you on the other side " + user_name + "." 
    slack_client.api_call("chat.postMessage", channel=get_channel_id(event_data), text=message)

@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
