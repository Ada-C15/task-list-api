from flask import current_app
from requests.models import parse_header_links
from app import db
import requests
import os


class Task(db.Model):
    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer,db.ForeignKey('goal.goal_id'),nullable = True)

    def serialize(self):
        result = {
            'id': self.task_id,
            'title': self.title,
            'description': self.description,
            'is_complete': self.completed_at != None
        } 
        if self.goal_id:
            result['goal_id'] = self.goal_id
        return result     

    # def serialize_two(self):
    #     result = {
    #         'id': self.task_id,
    #         'goal_id': self.goal_id,
    #         'title': self.title,
    #         'description': self.description,
    #         'is_complete': self.completed_at != None
    #     } 
    #     return result     

    def notify_slack(self):
        message = f"Someone just completed the task {self.title}"
        url = "https://slack.com/api/chat.postMessage"
        params = {
            
            "channel":"task-notifications",
            "text": message
        }
        headers = {
            "Authorization": os.environ.get('SLACK_API')
        }
        r = requests.post(url, data = params, headers = headers)
        r.status_code


  
    

