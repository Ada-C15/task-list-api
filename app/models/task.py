from flask import current_app
from app import db
import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True) 
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    
    # created a helper function to convert completed_at to is_complete.
    def to_json(self):
        if self.completed_at:
            complete = True
        else:
            complete = False

        regular_response = {

            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": complete
        }

        if self.goal_id is not None:
            regular_response["goal_id"] = self.goal_id

        return regular_response
    


    