from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)   # nullable allow an empty cell
    __tablename__ = "tasks"    #specifically for flask migrate
