from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    
    def to_json(self): 
        to_json = {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)
        }
        return to_json
    
    def tasks_to_json(self):
        reponse = self.to_json() 
        
        if self.goal_id: 
            reponse["goal_id"] = self.goal_id
            return reponse
        else: 
            return reponse

    def specific_task_to_json(self): 
        return {
            "task": self.tasks_to_json()
        }
    
    @classmethod
    def make_a_task(cls, json, id): 
        return cls(task_id=id,
                    title=json["title"],
                    description=json["description"], 
                    completed_at=json["completed_at"])
    
    def to_json_for_db(self): 
        to_json = {
                "task_id": self.task_id,
                "title": self.title,
                "description": self.description,
                "completed_at": self.completed_at
        }
        return to_json