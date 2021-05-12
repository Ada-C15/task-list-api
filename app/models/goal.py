from flask import current_app
from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # creating a relationship to the Task Model a virtual column named goals in the tasks table (will not affect the db) 
    tasks = db.relationship("Task", backref="goals", lazy=True)

    # This helps us find a goal's related tasks with goal.tasks
    # and a task's related goal with task.goals (as in goals table, not many goals)

    __tablename__= "goals"

    def to_dict(self):
        
        return {
            "id": self.id,
            "title": self.title
        }
