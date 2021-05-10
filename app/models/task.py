from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    # a task with a null value for completed_at has NOT been completed:
    completed_at = db.Column(db.DateTime, nullable=True)

    __tablename__= "tasks"

    def to_dict(self):
        if self.completed_at == None:
            # adds key to temp dict before we can return new_task
            is_complete = False
        else:
            is_complete = True
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }