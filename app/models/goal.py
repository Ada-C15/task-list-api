from flask import current_app
from app import db
#from .models.task import Task #wave 6

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    
    tasks = db.relationship('Task', backref='goal', lazy=True) #wave 6
    
    def to_json_goal(self):
        
        return {
                "goal":     
                       {
                            "id": self.goal_id,
                            "title": self.title,
                        }
                     }
    def to_json_goal_no_key(self):    
                return {
                            "id": self.goal_id,
                            "title": self.title
                        }