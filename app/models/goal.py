from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', backref='goal')

    def json_response(self):
        goal_response = {
            "id": self.goal_id,
            "title": self.title
        }
        return goal_response
