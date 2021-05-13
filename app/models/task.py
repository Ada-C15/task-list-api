from flask import current_app
from app import db
from sqlalchemy import DateTime
from app.models.goal import Goal

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goaltask_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    # creates a dictionary of key-value pairs describing the given task
    def to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if self.completed_at is None else True
        }