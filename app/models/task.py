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
    goal_id = db.Column(db.Integer, ForeignKey('goal.goal_id'), nullable=True, default=None)

    #def __init__(self, task_id):
        #self.task_id = task_id


    def to_json(self):
        return{
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if self.completed_at is None else True
        }

    