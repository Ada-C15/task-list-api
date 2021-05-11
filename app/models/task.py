from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .goal import Goal

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    # goals = db.Relationship("Goal", back_populates="tasks")

    __tablename__="task"
    def get_resp(self):
        if not self.goal_id:
            return{
                    "id": self.task_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": (False if self.completed_at == None else True )
                }
        else:
            return{
                    "id": self.task_id,
                    "goal_id": self.goal_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": (False if self.completed_at == None else True )
                }
    
    
