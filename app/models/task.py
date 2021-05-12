from flask import current_app
from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=True)
    __tablename__ = "tasks"

    def to_json(self):
        complete = False
        if self.completed_at:
            complete = True
        json_data = {"task":{
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": complete,
            "goal_id": self.goal_id}
        }
        # Lets beginning wave tests still pass
        if self.goal_id is None:
            del json_data["task"]["goal_id"]
        return json_data
    
    def to_string(self):
        return f"{self.id}: {self.title} Description: {self.description}"