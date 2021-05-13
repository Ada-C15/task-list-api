from flask import current_app
from app import db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    g_id = db.Column(db.Integer, db.ForeignKey('goal.g_id'), nullable=True)
    # __tablename__ = "tasks"

    def is_complete(self):
        if self.completed_at is None:
            is_complete = False
        else:
            is_complete = True
        return is_complete

    def to_json(self):
        if self.g_id:
            return{
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete" : self.is_complete(),
                "goal_id": self.g_id
            }
        else:
            return{
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete" : self.is_complete()
            }

    
