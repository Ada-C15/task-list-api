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
    # goal_id = db.Column(db.Integer, db.ForeignKey('goal_id'),
    #     nullable=True
    


    def is_complete(self): 
            if not self.completed_at: 
                return False
            return True