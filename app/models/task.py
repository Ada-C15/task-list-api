from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True, default = None)

    # Use is_complete as the output for completed_at
    def is_complete(self):
        return self.completed_at != None

    # Included completed_at to check if nullable is working
    def to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
        }
