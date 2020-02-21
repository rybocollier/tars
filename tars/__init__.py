import os
from flask import Flask, request, Response
from slackclient import SlackClient

# instantiate flask app
app = Flask(__name__)

# import environment variables
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET', None)

# instantiate slack client
slack_client = SlackClient(SLACK_TOKEN)


def list_channels():
    channels = slack_client.api_call("channels.list")

    if channels['ok']:
        return channels['channels']
    return None

def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='pythonbot',
        icon_emoji=':robot_face:'
    )

@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":
    app.run(debug=True, port=5000)


#if __name__ == "__main__":
#    channels = list_channels()
#
#    if channels:
#        for channel in channels:
#            print(channel['name'])
#            print(channel['id'])
#            send_message(channel['id'], "Hello " +
#            channel['name'] + "! It worked!")
#        
#    
#        print("Unable to authenticate.")
