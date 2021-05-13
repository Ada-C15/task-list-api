import random
import os
import requests

class GLaDOS():
    """Implements GLAdOS as a bot in Slack"""

    def __init__(self):
        self.messages = os.environ.get('GLA_DOS')
        self.path = "https://slack.com/api/chat.postMessage"
        self.channel = "task-notifications"
        self._quotes = [] 

    @property
    def get_random_quote(self):
        if self._quotes == []:
            with open("app/glados", "r") as quotes:
                read_quotes = quotes.readlines()
            for q in read_quotes:
                self._quotes.append(q.rstrip())

        return self._quotes[random.randint(0, len(self._quotes)-1)]

    def send_request(self, a_task):
        bot_msg = self.get_random_quote
        text = f"A human has just completed the task {a_task.title}.\n"\
            f"{bot_msg}"

        body = {
            "token": self.messages,
            "channel": self.channel,
            "text": text
        }
        polite_message = requests.post(self.path, data=body)
        return polite_message
