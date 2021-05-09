from flask import current_app
from app import db


class Goal(db.Model):
    # Goals are entities that describe a task a user wants to complete.
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }

    def tasks_to_dict(self):
        tasks_ids = []
        for task in self.tasks:
            tasks_ids.append(task.task_id)
        return {
            "id": self.goal_id,
            "task_ids": tasks_ids
        }
