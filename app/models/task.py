from flask import current_app
from app import db
from app.models.goal import Goal

#messages in video

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_identity = db.Column (db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
