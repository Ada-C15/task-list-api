from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .goal import Goal 


class Task(db.Model):
    __tablename__ = "task"
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    
    def to_json(self): 
        serialized = {
            "id": self.task_id,
            "title": self.title, 
            "description": self.description, 
            "is_complete": self.completed_at != None
        }
        # self.completed_at != None predicate to determine whether task is complete or not 

        if self.goal_id: 
            serialized["goal_id"] = self.goal_id

        return serialized

