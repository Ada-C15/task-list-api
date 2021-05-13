from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))

    # consider making separate function to determine if complete or not**
    
    # helper method to return dictionary and simultaneously 
    # report if task has been completed or not
    def to_dict(self):
        if self.goal_id:
            return {
            "id": self.task_id, 
            "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None
            }
        return {
            "id": self.task_id, 
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None
        }

