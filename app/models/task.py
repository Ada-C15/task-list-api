from flask import current_app
from app import db
from flask import request, Blueprint, make_response, jsonify


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, nullable = True)
    goals_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)