from app import db
from flask import current_app


class Task(db.Model):

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True) #autoincrement optional
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True) #nullable value
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def json_response(self):
        response = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
            }

        if self.goal_id:
            response["goal_id"] = self.goal_id

        return response

