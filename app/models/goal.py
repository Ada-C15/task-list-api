from flask import current_app
from app import db
from flask import request, Blueprint, make_response, jsonify


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    tasks = db.relationship("Task", backref="goal", lazy=True)
