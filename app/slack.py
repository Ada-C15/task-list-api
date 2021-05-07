import requests
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


def slack_message(message):
    path = "https://slack.com/api/chat.postMessage"

    query_params = {
        "channel": "task-notifications",
        "text": message
    }

    auth = os.environ.get('SLACK_BOT_TOKEN')
    # print(auth)

    headers = {
        "Authorization": f"Bearer {auth}"
    }

    request = requests.post(path,
                            headers=headers,
                            params=query_params
                            )

    return request.json()


# print(slack_message("Hello!"))
