from app.models import task
import requests 
import os


PATH = "https://slack.com/api/chat.postMessage"

API_KEY = os.environ.get("API_KEY")

def slack_bot_message(task):
    params = {"channel": "slackbot-project",
              "text": f"Someone just completed task {task.title}",
            
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.post(PATH, params=params, headers=headers)
    response_body = response.json()
    
    print(response_body)
    return response_body


