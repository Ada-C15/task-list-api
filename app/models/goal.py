from flask import current_app
from app import db
from sqlalchemy.orm import relationship




class Goal(db.Model):
    __tablename__ = 'goal'
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy=True)


    def json_response(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
        

