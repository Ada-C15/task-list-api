from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def task_response(self):
        task_response = {
            "task":{   
                "id": self.task_id,
                "title": self.title,    
                "description": self.description,
                "is_complete": bool(self.completed_at)
                }
            }
        if self.goal_id:
            task_response["goal_id"] = self.goal_id
        return task_response
    
    def task_response_lean(self):
        task_response = {
                "id": self.task_id,
                "title": self.title,    
                "description": self.description,
                "is_complete": bool(self.completed_at)
                }
        return task_response    
    
    