from flask import current_app
from app import db
from app.models.task import Task
from flask_sqlalchemy import SQLAlchemy

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy=True)
    __tablename__ = "goals"

    def to_json(self):
        task_list = [task.to_json()["task"] for task in self.tasks]

        json_data = {
            "id": self.id,
            "title": self.title,
            "tasks": task_list
        }
        # Only need this to keep wave 5 tests passing
        if not self.tasks:
            del json_data["tasks"]
        return json_data
    
    def to_string(self):
        return f"{self.id}: {self.title} Description: {self.description}"