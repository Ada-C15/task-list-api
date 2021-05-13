from flask import request, current_app
from app import db
# from app.models.goal import Goal


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", backref=db.backref("tasks"), lazy=True)

def to_dict(self):
    return {
        "id": self.task_id,
        "title": self.title,
        "description": self.description,
        "is_complete": bool(self.completed_at)
    }

def to_dict_goal(self):
    return {
        "id": self.task_id,
        "goal_id": self.goal_id,
        "title": self.title,
        "description": self.description,
        "is_complete": bool(self.completed_at)
    }


# def completed_task(self):
#     if self.completed_at == None:
#         completed = False
#     else:
#         completed = True




