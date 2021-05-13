from flask import current_app
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)

    def complete_task(self):
        if self.completed_at == None:
            return False
        else: 
            return True

    def to_json(self):
        if self.goal_id:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.complete_task(),
                "goal_id": self.goal_id
            }
        else:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.complete_task()
            }