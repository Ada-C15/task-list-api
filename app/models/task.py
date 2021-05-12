from flask import current_app
from app import db
# from app.models.goal import Goal


class Task(db.Model):
    # To pass tests: can change task_id name, but all other columns must keep same names
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    matching_goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),nullable=True)

    # this method returns a dictionary of attribute values for a Task model instance, as well as a True or False value depending on whether the task has a completed_at time stamp
    def convert_to_json(self):
        return {  
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
            
        }
