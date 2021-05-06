from flask import current_app
from app import db
import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

# customized 'to_json' method - made all tests pass
    def to_json(self):
        check_completion = False

        if self.completed_at:
            check_completion = True
        
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": check_completion # was "completed_at": check_completion >> changed to pass test 2
        }
