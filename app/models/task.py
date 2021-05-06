from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)



    # helper function that gives is_complete a value to use in the is_complete and returns dict of task instances
    def to_json(self):
        if self.completed_at == None:
            is_complete = False
        else:
            is_complete = True 
            
        return {
        "id": self.task_id,
        "title": self.title,
        "description": self.description,
        "is_complete": is_complete
        }