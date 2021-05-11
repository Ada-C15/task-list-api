from flask import current_app
from app import db



class Task(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(250))
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.goal_id"), nullable=True)

    def to_json(self):
        task_dictionary = {"id": self.task_id, 
                        "title": self.title, 
                        "description": self.description, 
                        "is_complete": False}
        if self.goal_id is None:
            return task_dictionary
        else:
            task_dictionary["goal_id"] = self.goal_id
            return task_dictionary

    def is_complete(self):
        if self.completed_at:
            return True
        else:
            return False