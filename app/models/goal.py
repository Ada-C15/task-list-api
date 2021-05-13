from flask import current_app
from sqlalchemy.orm import backref
from app import db


class Goal(db.Model):
    __tablename__ = 'goal'
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def to_json_goal(self):
        # This method was created so that we do not have to write out the dictionary many times in the routes.py file. 
        return {
            "id": self.goal_id,
            "title": self.title,
        }

