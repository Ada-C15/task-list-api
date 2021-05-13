from flask import current_app
from app import db
from sqlalchemy.orm import relationship


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", lazy=True)

    def goal_json(self):
        return {"goal": {
            "id" : self.goal_id,
            "title" : self.title
        }}