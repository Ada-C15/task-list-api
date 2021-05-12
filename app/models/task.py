from flask import current_app
from app import db

# child class 
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True, default = None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
    goal=db.relationship("Goal",backref=db.backref('task',lazy=True))

    
    # helper function that will find out if a task has been completed or not
    def is_completed(self):
        return self.completed_at != None      
    # helper function to output for response body 
    def to_json(self):
        return {
            "id": self.task_id,
            "goal_id":self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_completed()
        }   


