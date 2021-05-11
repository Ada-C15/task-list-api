from flask import current_app
from app import db
from sqlalchemy.orm import relationship
from .task import Task


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy=True)

    #backref meaning: creates a column in the Task table called "goal"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
