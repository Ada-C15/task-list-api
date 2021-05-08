from flask import current_app
from app import db
import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True) 
    
    # created a helper function to conver completed_at to is_complete.
    def to_json(self):
        if self.completed_at:
            complete = True
        else:
            complete = False

        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": complete
        }



    