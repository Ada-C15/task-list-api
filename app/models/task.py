from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(250))
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        return {"id": self.task_id, 
                "title": self.title, 
                "description": self.description, 
                "is_complete": False}

    def is_complete(self):
        if self.completed_at:
            return True
        else:
            return False