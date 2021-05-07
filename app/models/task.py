from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def is_task_complete(self):
        if not self.completed_at:
            return False
        return True

    def get_task_info(self):
        task_info = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_task_complete(),
        }
        if self.goal_id:
            task_info['goal_id'] = self.goal_id
        return task_info