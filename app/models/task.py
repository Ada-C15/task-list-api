from flask import current_app
from app import db
from sqlalchemy.orm import relationship


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def task_completed(self):
        if self.completed_at:
            return True
        else:
            return False

    def return_task_json(self):
        task_dict = {
        "id" : self.task_id,
        "title" : self.title,
        "description": self.description,
        "is_complete":self.task_completed()
        }
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict
