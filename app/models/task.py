from flask import current_app
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_json(self):

        # Task.completed_at != None
        # use return to return dictionaries
        # use jsonify to return arrays
        # make_resp should work similarly to jsonify

        return {
            "task": {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at != None
                }
        }, 201




