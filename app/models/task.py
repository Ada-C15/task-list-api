from flask import current_app
from app import db


class Task(db.Model):
    # can change task_id name, but all other columns must keep same names
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
