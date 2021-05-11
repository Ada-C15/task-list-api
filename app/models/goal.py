from flask import current_app
from app import db
#from app.models.task import Task #is this necessary?


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
