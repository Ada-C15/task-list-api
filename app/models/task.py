from flask import current_app
from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(100))
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_json(self): # return proper format
        if self.completed_at:
            check_completion = True
        else:
            check_completion = False

        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": check_completion
            }