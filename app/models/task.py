from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True,)#default=False
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
#have two methods here, or one
#one that checks is complete or none
#one that makes a jasonified response for if the completed is true and shows that to the user 
#using the completed at self as a param

#Task.completed_at!= None
    def to_json(self):
        # if self.completed_at == None:
        #     is_complete = False
        # else:
        #     is_complete = True
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None
        }

    

