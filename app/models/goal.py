from flask import current_app
from sqlalchemy.orm import backref
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    task = db.relationship('Task', backref='goaltask', lazy=True)

    def goal_json(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
