import hashlib
import hmac
import os
import sys
import time
from flask import Flask, request, Response
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter

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
    event = event_data["event"]

    # match user ID to user name
    user_data = slack_client.api_call(
        "users.info",
        token=SLACK_TOKEN,
        user=event["user"],
    )

    # match channel ID to channel name
    channel_data = slack_client.api_call(
        "channels.info",
        token=SLACK_TOKEN,
        channel=event["channel"],
    )

    message = "Welcome " + user_data["user"]["name"] + " to " + channel_data["channel"]["name"] + "!"

    slack_client.api_call("chat.postMessage", channel=event["channel"], text=message)

    return event

@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
