from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    # __tablename__ = "tasks"

    def to_json(self):
        is_complete = None
        if self.completed_at is None:
            is_complete = False
        else:
            is_complete = True
        return{
            "id": self.id,
            "title": self.title,
            "description": self.description,
            #"is_complete": self.completed_at
            "is_complete" : is_complete
        }

    
