from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
# from .task import Task

# One-to-many - Goal has many tasks, so goal is the parent. 
# pull tasks from goal. 
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    __tablename__="goal"
    # tasks = db.Relationship("Task", back_populates="goals")
    tasks = db.relationship("Task", backref="goals", lazy=True)

    def get_resp(self):
        if not self.tasks:
            return{
                    "id": self.goal_id,
                    "title": self.title,
                    "tasks": []
                }
        else:
            return{
                    "id": self.goal_id,
                    "title": self.title,
                    # "tasks": self.tasks
                }
                