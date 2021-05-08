from flask import current_app
from app import db
from sqlalchemy.orm import relationship
from .task import Task


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    title = db.Column(db.String)
    tasks = relationship("Task", lazy=True)

    def to_dict(self):
        return {"id": self.goal_id,
                "title": self.title}
