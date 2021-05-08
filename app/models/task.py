from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    # a task with a null value for completed_at has NOT been completed:
    completed_at = db.Column(db.DateTime, nullable=True)

    __tablename__= "tasks"
