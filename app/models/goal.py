from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # whatever I put in the backref in creates a fake column in the Task table noted in the argument before backref?
    #tasks is going to be a list of Task instances. its called an iterator 
    #lazy= true  means that it will return all data assigned to the object even if you use a key as a referen
    tasks = db.relationship("Task", backref='task', lazy=True)
    
    
    def goal_to_json(self):
        """
            Input:  instance of Goal
            Output: returns python dictionary of instance of Goal
        """
        return {
            "id": self.goal_id,
            "title": self.title,
        }
    
    
