from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # whatever I put in the backref in creates a fake column in the Task table noted in the argument before backref?
    #tasks is going to be a list of Task instances. its called an iterator 
    tasks = db.relationship("Task", backref='task', lazy=True)
    
    #helper function to return in json format
    def goal_to_json(self):
        
        return {
        "id": self.goal_id,
        "title": self.title,
        }
    
    
