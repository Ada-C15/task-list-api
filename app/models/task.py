from flask import request, current_app
from app import db
# from app.models.goal import Goal


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))

def to_dict(self):
    return {
        "id": self.task_id,
        "title": self.title,
        "description": self.description,
        "is_complete": bool(self.completed_at)
    }

# def completed_task(self):
#     if self.completed_at == None:
#         completed = False
#     else:
#         completed = True




