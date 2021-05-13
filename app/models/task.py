from flask import current_app
from app import db
from dataclasses import dataclass 
from datetime import datetime
from typing import Optional

@dataclass
class Task(db.Model):
    id: int 
    title: str 
    description: str 
    completed_at: Optional[datetime]

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),nullable=True)
    


    def is_complete(self): 
            if not self.completed_at: 
                return False
            return True

    def as_json(self):

        result_dict = {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
            }

        if self.goal_id: 
            result_dict["goal_id"] = self.goal_id
        
        return result_dict

    @classmethod
    def from_json(cls,task_dict):

        return Task(title = task_dict["title"],
                description = task_dict["description"],
                completed_at = task_dict["completed_at"])
        

        