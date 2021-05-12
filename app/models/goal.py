from flask import current_app
from app import db
# from app.models.task import Task



class Goal(db.Model):
    # Feel free to change the name of the goal_id column if you would like. The tests require the title column to be named exactly as title.
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    # this method returns a dictionary of attribute values for a Task model instance, as well as a True or False value depending on whether the task has a completed_at time stamp
    def convert_to_json(self):
        return {  
            "id": self.goal_id,
            "title": self.title
        }

