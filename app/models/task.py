from flask import current_app
from sqlalchemy.orm import backref
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title= db.Column(db.String)
    description= db.Column(db.String)
    completed_at=db.Column(db.DateTime, nullable=True, default=None)
    
#establishing one to many relationship with Goal
    goal_id = db.Column(db.Integer,db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal",backref=db.backref('tasks'),lazy=True)

#returns True when there is a task completed
    def is_complete(self):
        if self.completed_at==None:
            return False
        else:
            return True

#runs to determine which body to return based on goal bool status
    def to_json(self):
        if self.goal_id == None:
            task_dict={
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
            }
        else:
           task_dict={
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
            } 
        return task_dict
    
