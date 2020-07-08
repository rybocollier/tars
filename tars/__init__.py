import json
import os
import sys
import time
from flask import Flask, request, Response
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter

# import tars skills
from tars.skills.data.commands import load_commands
from tars.skills.reddit.til import (
    get_random_til,
    generate_til_message_block,
    send_til_message,
)
from tars.skills.openweather.weather import (
    get_weather_details,
    get_zipcode,
    generate_weather_message_block,
    send_weather_message,
)
from tars.skills.slack.user import get_user_id, get_user_name
from tars.skills.slack.channel import get_channel_id, get_channel_name

# instantiate flask app
app = Flask(__name__)

# import environment variables
SLACK_TOKEN = os.environ.get("SLACK_TOKEN", None)
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET", None)
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", None)
OPENWEATHER_ENDPOINT = os.environ.get("OPENWEATHER_ENDPOINT", None)

# instantiate slack client
slack_client = SlackClient(SLACK_TOKEN)


def print_debug(input):
    print(input, file=sys.stderr)


slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)


@slack_events_adapter.on("member_joined_channel")
def member_joined(event_data):
    # match user ID to user name
    user_name = get_user_name(slack_client, SLACK_TOKEN, get_user_id(event_data))
    message = "Hello " + user_name + "."
    slack_client.api_call(
        "chat.postMessage", channel=get_channel_id(event_data), text=message
    )


@slack_events_adapter.on("member_left_channel")
def member_left(event_data):
    # match user ID to user name
    user_name = get_user_name(slack_client, SLACK_TOKEN, get_user_id(event_data))
    message = "See you on the other side " + user_name + "."
    slack_client.api_call(
        "chat.postMessage", channel=get_channel_id(event_data), text=message
    )


@slack_events_adapter.on("app_mention")
def conversation_router(event_data):
    message_text = event_data["event"]["text"]
    message_list = message_text.split()
    command = message_list[1].lower()

    # load commands
    commands = load_commands()

    # verify that the command specified is supported
    if command in commands:
        if command == "til":
            til_post = get_random_til()

            message = generate_til_message_block(til_post)

            send_til_message(
                slack_client, get_channel_id(event_data), til_post, message
            )
        if command == "weather":
            zipcode = get_zipcode(message_list)

            weather_response = get_weather_details(
                zipcode, OPENWEATHER_API_KEY, OPENWEATHER_ENDPOINT
            )

            message_block = generate_weather_message_block(weather_response)

            send_weather_message(
                slack_client, get_channel_id(event_data), message_block
            )

            print_debug(weather_response)
    else:
        message = "Command not supported."
        slack_client.api_call(
            "chat.postMessage", channel=get_channel_id(event_data), text=message
        )


@app.route("/", methods=["GET"])
def test():
    return Response("It works!")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
