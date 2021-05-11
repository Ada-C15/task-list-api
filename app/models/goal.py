from flask import current_app
from app import db
from dataclasses import dataclass 


@dataclass
class Goal(db.Model):
    goal_id: int 
    title: str 




    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # tasks = db.relationship('Task', backref='goal', lazy=True)


