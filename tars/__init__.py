import hashlib
import hmac
import os
import sys
import time
from flask import Flask, request, Response
from slackclient import SlackClient

# instantiate flask app
app = Flask(__name__)

# import environment variables
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET', None)

# instantiate slack client
slack_client = SlackClient(SLACK_TOKEN)

def print_debug(input):
    print(input, file=sys.stderr)

@app.route('/slack', methods=['POST'])
def verify_request():
    slack_signing_secret = SLACK_SIGNING_SECRET
    request_data = request.get_data()
    challenge_timestamp = request.headers['X-Slack-Request-Timestamp']
    slack_signature = request.headers['X-Slack-Signature']
    
    if abs(time.time() - int(challenge_timestamp)) > 60 * 5:
        return

    sig_basestring = str.encode('v0:' + str(challenge_timestamp) + ':') + request_data

    tars_signature = 'v0=' + hmac.new(
        str.encode(slack_signing_secret),
        sig_basestring, hashlib.sha256
    ).hexdigest()

    if hmac.compare_digest(tars_signature, slack_signature):
        return request_data
    
    return False

@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
