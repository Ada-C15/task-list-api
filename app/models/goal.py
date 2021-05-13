from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    # This instance method returns a JSON dictionary of attribute values 
    # with an optional argument if the goal has tasks assigned to it
    def convert_to_json(self, tasks_list=None):

        response_body = {  
            "id": self.goal_id,
            "title": self.title
        }

        if tasks_list != None:
            response_body["tasks"] = tasks_list

        return response_body
