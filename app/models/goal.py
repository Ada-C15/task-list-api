from flask import current_app
from app import db

# Our task list API should be able to work with an entity called Goal.

# ****Goals are entities that describe a task a user wants to complete.****

# They contain a title to name the goal.

# Our goal for this wave is to be able to create, read, update, and delete different goals.

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref='goal', lazy=True) #originally had task and not tasks

    def now_json(self):
        return{
            "id": self.goal_id,
            "title": self.title,
        }
