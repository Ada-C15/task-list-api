from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)


    # helper function that gives is_complete a value to use in the is_complete and returns dict of task instances
    def to_json(self):
        if self.completed_at == None:
            is_complete = False
        else:
            is_complete = True 
            
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
    
    #adding "goal_id" key to the returning value from our to_json() helper function 
    def to_json_goal_id(self):
        result = self.to_json()
        result["goal_id"] = self.goal_id
        return result 