from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)


    def is_complete(self):
        if self.completed_at is None:
            return False
        else:
            return True

    def to_dict(self):
        return {
            "id": self.task_id, 
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at()
            }   

    def to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed_at": False if self.completed_at is None else True
        }

    def to_json_goal_id(self):
        return {
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": False if self.completed_at is None else True
            }