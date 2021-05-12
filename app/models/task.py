from flask import current_app
from app import db

#WAVE 1
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def task_to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": (False if self.completed_at == None else True)
            }        

    
    def to_string(self):
        return f"{self.task_id}: {self.title} Description: {self.description} Completed at: {self.completed_at} "
