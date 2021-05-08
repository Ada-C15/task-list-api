from flask import current_app
# from .goal import Goal
from app import db


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
        else:
            return True

    def goal_id_to_json(self):
        return {
            "goal_id": self.goal_id
        }
    

    def to_json(self):
        # is_complete = None
        # if not self.completed_at:
        #     is_complete = False
        # else:
        #     is_complete = True

        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.check_is_complete(),
        }