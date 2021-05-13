from flask import current_app
from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref="goal", lazy=True)

    def to_json_goal(self):
        if self.tasks:
            return {
                "id": self.goal_id,
                "title": self.title,
                "tasks": self.tasks
            }
        else:
            return {
                "id": self.goal_id,
                "title": self.title
            }


    