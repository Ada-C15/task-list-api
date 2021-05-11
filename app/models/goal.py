from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # addresses = db.relationship('Address', backref='person', lazy=True)
    tasks = db.relationship('Task', backref='goal', lazy=True)
    # backref=db.backref('person', lazy='joined'))
    
    
    def to_json(self):

        return {
            "goal": {
                "id": self.goal_id,
                "title": self.title,
                }
        }

