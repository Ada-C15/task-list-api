from flask import current_app
from app import db
from app.models.goal import Goal

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goals_id = db.Column(db.Integer, db.ForeignKey("goals.goal_id"), nullable=True)
    __tablename__ = "tasks"

    def to_json(self):
        if self.completed_at:
            is_completed = True
        else:
            is_completed = False
        task_dictionary={
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_completed
        }
        if self.goals_id:
            task_dictionary["goal_id"]= self.goals_id
        return task_dictionary