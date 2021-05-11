from flask import current_app
from app import db

#user in video


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Message', backref="goal", lazy=True)

    
