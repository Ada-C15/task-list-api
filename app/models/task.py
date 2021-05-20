from flask import current_app
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_num = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable = True)

    def is_complete(self):
        if self.completed_at is None:
            return False
        else:
            return True
    
    def to_json(self):
        return {
        "id": self.task_id, 
        "title": self.title,
        "description": self.description,
        "is_complete": self.is_complete(),
        } 
