from flask import current_app
from sqlalchemy.orm import backref
from app import db
#from sqlalchemy.types import DateTime
#from app.models.goal import Goal

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title= db.Column(db.String)
    description= db.Column(db.String)
    completed_at=db.Column(db.DateTime, nullable=True, default=None)
    

    __tablename__='task'
    goal_id=db.Column(db.Integer,db.ForeignKey('goal.goal_id'), nullable=True)
    goal=db.relationship("Goal",backref=db.backref('tasks'),lazy=True)
    #goal=db.relationship("Goal",back_populates='child_tasks')

#runs when there is a task completed
    def is_complete(self):
        if self.completed_at==None:
            return False
        else:
            return True