from app import db
from flask import current_app, jsonify

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    __tablename__ = "tasks"

    def to_json(self):
        if self.completed_at == None:
            completed_at = self.completed_at
            completed_at = False
        elif self.completed_at != None:
            completed_at = self.completed_at
            completed_at = True
            
        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": completed_at
            }
