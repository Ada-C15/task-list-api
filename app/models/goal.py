from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    # Establishing one to many relationships to Task Model by adding
    # tasks ==>  like person to dogs
    tasks = db.relationship('Task', backref="goal", lazy=True)
    
    def goal_to_json_response(self):
        return {"goal": 
                        {"id": self.goal_id,
                        "title": self.title}}

    def simple_response(self):
        return {"id": self.goal_id,
                "title": self.title}


