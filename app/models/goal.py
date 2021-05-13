from types import new_class
from flask import current_app
from app import db
from app.models.task import Task
# Parent Class


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def goal_json_object(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }

    def goal_json_object_with_tasks(self):
        new_list = []
        for task in self.tasks:
            new_list.append({
                "id": task.id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at_helper()
            })
        return {
            "id": self.goal_id,
            "title": self.title,
            "tasks": new_list
        }
