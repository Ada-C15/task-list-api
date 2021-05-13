from flask import current_app
from app import db


class Task(db.Model):
    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)   # nullable allow an empty cell
    
    goal_id = db.Column(db.Integer,db.ForeignKey("goals.goal_id"), nullable=True)
    
    def is_complete(self):
        completed_at = self.completed_at
        if completed_at == None:
            is_complete = False
        else:
            is_complete = True
        return is_complete