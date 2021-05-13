from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='tasks', lazy=True)


    def goal_dict(self):
        return{   
                "id": self.goal_id,
                "title": self.title,
                                        }