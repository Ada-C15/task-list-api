from app import db
from flask import current_app, jsonify

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    __tablename__ = "tasks"

    def to_json(self):
        if self.completed_at is None:
            self.completed_at = False
            
        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at
            }
