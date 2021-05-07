from flask import current_app
from app import db
from flask import jsonify


class Task(db.Model):
    __tablename__ = "task"
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = True if completed_at is True else False   
    # if completed_at is not None:
    #     is_complete == True

    def to_json_format(self):
        task_to_json = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete,
            }
        if self.completed_at is not None:
            task_to_json["completed_at"] = self.completed_at
        return task_to_json

# "completed_at": self.completed_at,