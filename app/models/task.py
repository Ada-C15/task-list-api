from flask import current_app
from app import db


class Task(db.Model):
    __tablename__ = "tasks"
    
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=True)


    def to_json(self):
        if self.goal_id == None:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete(),
            }
        else:
            return {
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete(),
            }


    def is_complete(self):
        completed_at = self.completed_at
        if completed_at == None:
            is_complete = False
        else:
            is_complete = True
        return is_complete