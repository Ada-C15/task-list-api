from flask import current_app
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    is_complete = False

    # def is_complete(self):
    #     if icomplete == None:
    #         return False
    #     else: 
    #         return True

    def complete_task(self):
        if self.completed_at == None:
            return False
        else: 
            return True


    def to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.complete_task() 
            # "is_complete": self.completed_at !=None
        }