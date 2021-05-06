from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    # def task_completed(self):
    #     is_complete = None
    #     if self.completed_at == None:
    #         is_complete = False
    #     else:
    #         is_complete = True
    
    def task_completed(self):
        if self.completed_at == None:
            return False
        else:
            return True 