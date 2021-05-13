from flask import current_app
from app import db
import datetime


class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)


    def to_json(self):
        if self.completed_at != None:
            result = self.completed_at
            result = True
        elif self.completed_at == None:
            result = self.completed_at
            result = False
        
        # This method was created so that we do not have to write out the dictionary many times in the routes.py file.
        if self.goal_id == None:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                # Not sure if I should change this part to make if completed_at is null is_complete is False
                "is_complete": result
            }
        else:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                # Not sure if I should change this part to make if completed_at is null is_complete is False
                "is_complete": result,
                "goal_id": self.goal_id

            }