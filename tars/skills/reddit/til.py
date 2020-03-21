import random
import requests
import json


def get_random_til():
    post = {}

    tars_headers = {'user-agent':'tars/0.1'}
    request = requests.get('https://reddit.com/r/todayilearned.json', headers=tars_headers)
    til_data = json.loads(request.text)
    
    random_post = random.randrange(25) 
    til_post = til_data['data']['children'][random_post]
    
    post_author = til_post['data']['author']
    post_title = til_post['data']['title']
    post_score = til_post['data']['score']
    post_url = til_post['data']['url']

    post.update( {'author':post_author} )
    post.update( {'title':post_title} )
    post.update( {'score':post_score} )  
    post.update( {'url':post_url} )  

    return post