from flask import current_app
from app import db
from flask_sqlalchemy import SQLAlchemy

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=True)
    __tablename__ = "tasks"

    def to_json(self):
        # refactor to format {task: {dict}}, then change all return statements
        complete = False
        if self.completed_at:
            complete = True
        json_data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": complete,
            "goal_id": self.goal_id
        }
        if self.goal_id is None:
            del json_data["goal_id"]
        return json_data
    
    def to_string(self):
        return f"{self.id}: {self.title} Description: {self.description}"