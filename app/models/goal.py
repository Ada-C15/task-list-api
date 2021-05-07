from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
# from .task import Task 
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    __tablename__ = "goal"
    tasks = db.relationship("Task", backref="goals")

    def to_json(self): 
        return {
            "id": self.goal_id,
            "title": self.title
        }
    