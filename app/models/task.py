from flask import current_app
from app import db
from sqlalchemy import DateTime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    # populates is_complete value depending on completed_at value
    def is_complete(self):
        if self.completed_at == None:
            return False
        else:
            return True

    # creates a dictionary of key-value pairs describing the given task
    def to_json(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at,
            "is_complete": self.is_complete
        }
