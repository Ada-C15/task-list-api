import requests
from dotenv import load_dotenv
import os
load_dotenv()

def slack_message(message):
    path = 'https://slack.com/api/chat.postMessage'
    query_params = {
        "channel": "bot-testing",
        "text": message
    }
    headers = {
        "Authorization": f'{os.environ.get("SLACK_API_KEY")}'
    }
    message = requests.post(path, params=query_params, headers=headers)
    return message.json()
