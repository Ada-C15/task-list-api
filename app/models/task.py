from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    description = db.Column(db.String(32))
    completed_at = None  # db.Column(db.DateTime)
    # A task with a null value for completed_at has not been completed.
    is_complete = False
