from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    __tablename__="goal"
    tasks = db.relationship("Task", backref="goals", lazy=True)

    def get_resp(self):
        return{
                    "id": self.goal_id,
                    "title": self.title,
                }
