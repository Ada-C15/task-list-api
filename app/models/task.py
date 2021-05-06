from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)

#write code to adjust completed at to true or false
    def task_completed(self):
        if self.completed_at:
            return True
        else:
            return False

    def return_task_json(self):
        return  {"task": {
        "id" : self.task_id,
        "title" : self.title,
        "description": self.description,
        "is_complete":self.task_completed()
        }}
