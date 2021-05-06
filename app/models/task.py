from flask import current_app
from app import db
import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    __tablename__ = "tasks"

    def to_json(self):
        complete = False
        if self.completed_at:
            complete = True
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": complete
        }
    
    def to_string(self):
        return f"{self.id}: {self.title} Description: {self.description}"