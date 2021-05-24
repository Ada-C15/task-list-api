from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    match_goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),nullable=True)

    
    # This instance method checks if a task has been completed, and whether it 
    # has a matching goal id, then returns a JSON dictionary of attribute values 
    def convert_to_json(self):

        response_body = { 
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
            }

        if self.match_goal_id:
            response_body["goal_id"] = self.match_goal_id

        return response_body
