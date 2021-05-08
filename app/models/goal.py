from flask import current_app
from app import db
from sqlalchemy.orm import relationship
from .task import Task


class Goal(db.Model):
    __tablename__ = "goal"
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy=True)

    def tasks_to_json(self):
        return {
            "tasks": self.tasks
        }

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }

