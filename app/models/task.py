from flask import current_app
from app import db
from .goal import Goal
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey



class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, ForeignKey('goal.goal_id'), nullable=True)


    def to_json(self):

        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if self.completed_at is None else True
        }

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    

    