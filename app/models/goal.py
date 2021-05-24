from flask import current_app
from app import db


class Goal(db.Model):
    # Goals are entities that describe a task a user wants to complete.
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def to_json(self):
        response_body = {
            "id": self.goal_id,
            "title": self.title
        }

        if len(self.tasks) != 0:
            tasks_ids = [task.task_id for task in self.tasks]
            response_body = {
                "id": self.goal_id,
                "task_ids": tasks_ids
            }

        return response_body
