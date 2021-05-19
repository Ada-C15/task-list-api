from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    title = db.Column(db.String, nullable = False)
    tasks = db.relationship(
        'Task', backref='goal', lazy=True
    )
    # task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    def serialize(self):
        result = {
            'id': self.goal_id,
            'title': self.title
        }
        return result
