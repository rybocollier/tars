import json
import requests
import sys
from datetime import datetime


def get_zipcode(message_list):
    try:
        zipcode = int(message_list[2])
    except ValueError:
        return False

    return zipcode


def get_weather_details(zipcode, api_key, openweather_endpoint):
    zip_country = str(zipcode) + "," + "us"
    params = {"zip": zip_country, "appid": api_key, "units": "imperial"}

    try:
        openweather_request = requests.get(openweather_endpoint, params=params)
    except:
        print("oops")
    else:
        openweather_request = json.loads(openweather_request.text)

    return openweather_request


def generate_weather_message_block(openweather_data):
    message_block = json.dumps(
        [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Here is your weather snapshot for "
                    + openweather_data["name"]
                    + "*",
                },
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Current Temperature*\n"
                        + str(openweather_data["main"]["temp"]),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Today's Low*\n"
                        + str(openweather_data["main"]["temp_min"]),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Today's High*\n"
                        + str(openweather_data["main"]["temp_max"]),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Humidity*\n"
                        + str(openweather_data["main"]["humidity"])
                        + "%",
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Wind Speed*\n"
                        + str(openweather_data["wind"]["speed"]),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Sunrise (UTC)*\n"
                        + datetime.utcfromtimestamp(
                            openweather_data["sys"]["sunrise"]
                        ).strftime("%Y-%m-%d %H:%M:%S"),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Sunset (UTC)*\n"
                        + datetime.utcfromtimestamp(
                            openweather_data["sys"]["sunset"]
                        ).strftime("%Y-%m-%d %H:%M:%S"),
                    },
                ],
            },
        ]
    )
    return message_block


def send_weather_message(slack_client, channel_id, message_block):
    response = slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        blocks=message_block,
        text="Weather info",
    )

    print(response, file=sys.stderr)

    return response
