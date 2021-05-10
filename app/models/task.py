from flask import current_app, jsonify
from app import db



class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def is_complete(self):
        if self.completed_at:
            return True
        return False

    def build_dict(self):
        if self.goal_id:

            return {
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
            }
        else:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
            }