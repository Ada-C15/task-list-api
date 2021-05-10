from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    

    def to_json(self):
        result = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None
        }
        if self.goal_id:
            result["goal_id"] = self.goal_id
        return result
