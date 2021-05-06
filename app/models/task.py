from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    # A task with a null value for completed_at has not been completed.
    __name__ = "tasks"

    def is_complete(self):
        if self.completed_at is None:
            return False
        else:
            return True
