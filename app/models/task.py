from flask import current_app
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime(), nullable=True)

    goal_id = db.Column(db.Integer, ForeignKey('goal.goal_id'), nullable=True, default=None)

    def as_dict(self):
        task = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }
        
        if self.goal_id:
            task["goal_id"] = self.goal_id

        return task
