from flask import current_app
from sqlalchemy.orm import relationship
from .task import Task
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    task = relationship("Task")

    def as_dict(self):
        return {"id": self.goal_id,
                "title": self.title}
