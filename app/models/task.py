from flask import current_app
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def check_if_complete(self):
        
        if self.completed_at == None:
            return False
        else:
            return True

    def to_json(self):

        if self.goal_id == None:

            return {
                "task": {
                    "id": self.task_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": self.check_if_complete()
                    }
            }

        else:

            return {
                "task": {
                    "id": self.task_id,
                    "goal_id": self.goal_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": self.check_if_complete()
                    }
            }



