from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # do i set it to autoincrement?
    title = db.Column(db.String) # or title (this is the name of the task)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    def to_json_response(self):
        return {"task": 
                        {"id": self.id,
                        "title": self.title,
                        "description": self.description,
                        "is_complete": bool(self.completed_at)}
                } 
    

