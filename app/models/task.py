from flask import current_app
# from .goal import Goal
from app import db
import json


class Task(db.Model):
    __tablename__ = "task"
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)

    def check_is_complete(self):
        if not self.completed_at:
            return False
        return True
    
    def to_json(self):
        task_json = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.check_is_complete(),
        }
        if self.goal:
            task_json["goal_id"] = self.goal_id
        return task_json

    # def from_json(cls):


    #     task_body = json.loads('{"__task__": "Task", "id": "task_id",\
    #                         "title": "title",
    #                         "description": "description",
    #                         "is_complete": "completed_at"}')
        


