from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref ='goal', lazy=True)

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }

    def to_json_with_tasks(self, tasks):
        return {
        "id": self.goal_id,
        "title": self.title,
        "tasks": tasks
    }