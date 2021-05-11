from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    # A task with a null value for completed_at has not been completed.
    # __tablename__ = "tasks"
    goal_id = db.Column(
        db.Integer,
        db.ForeignKey('goal.goal_id'),
        nullable=True)

    def is_complete(self):
        if self.completed_at is None:
            return False
        else:
            return True

    def to_dict(self):
        response_body = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
        }

        if self.goal_id:
            response_body["goal_id"] = self.goal_id

        return response_body
