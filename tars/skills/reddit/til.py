import json
import random
import requests
import time


def get_random_til():
    post = {}

    tars_headers = {'user-agent':'tars/0.1'}
    request = requests.get('https://reddit.com/r/todayilearned.json', headers=tars_headers)
    til_data = json.loads(request.text)
    
    random_post = random.randrange(30) 
    til_post = til_data['data']['children'][random_post]
    
    post_author = til_post['data']['author']
    post_title = til_post['data']['title']
    post_score = til_post['data']['score']
    post_url = til_post['data']['url']
    post_thumbnail = til_post['data']['thumbnail']
    subreddit_name_prefixed = til_post['data']['subreddit_name_prefixed']
    created_at = til_post['data']['created']
    comments = til_post['data']['permalink']

    created_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created_at)) 

    post.update( {'author':post_author} )
    post.update( {'title':post_title} )
    post.update( {'score':post_score} )
    post.update( {'url':post_url} )
    post.update( {'thumbnail':post_thumbnail} )
    post.update( {'subreddit_name_prefixed':subreddit_name_prefixed} )
    post.update( {'created':created_datetime} )
    post.update( {'permalink':"https://reddit.com" + comments} )

    return post

def generate_message_block(post):
    til_post = post 
    message_block = json.dumps([
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Here is your random TIL from user " + til_post['author'] + " on " + til_post['subreddit_name_prefixed'] 
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "<" + til_post['url'] + "|" + til_post['title'] + ">"
            },
            "accessory": {
                "type": "image",
                "image_url": til_post['thumbnail'],
                "alt_text" : til_post['title']
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Created on*\n" + str(til_post['created'])
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Comments* \n" + til_post['permalink']
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Karma*\n" + str(til_post['score'])
                }
            ]
        }
    ])
    return message_block 

def send_til_message(slack_client, channel_id, post, message_block):
    response = slack_client.api_call("chat.postMessage",
        channel=channel_id,
        blocks=message_block,
        text=post['title'],
    )

    return response
