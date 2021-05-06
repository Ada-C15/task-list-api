from flask import current_app
from app import db
from flask import Blueprint


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(50)) 
    completed_at = db.Column(db.DateTime, nullable=True)
    