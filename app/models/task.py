from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def to_json_format(self):
        task_to_json = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at is not None else False,
        }
        if self.goal is not None:
            task_to_json["goal_id"] = self.goal
        return task_to_json


