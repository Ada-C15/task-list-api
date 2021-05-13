from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # 'Task' looks at class in python and loads multiple of those (this is like a pseudo column)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }
