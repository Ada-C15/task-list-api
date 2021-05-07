from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        # This method was created so that we do not have to write out the dictionary many times in the routes.py file. 
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            # Not sure if I should change this part to make if completed_at is null is_complete is False
            "is_complete": False
        }