from flask import current_app
from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    tasks = db.relationship("Task", backref="goals", lazy=True)
    __tablename__ = "goals"
    
    def to_json(self):
        if self.tasks != []:
            return {
                "id": self.goal_id,
                "title": self.title,
                "tasks": self.tasks
            }
        else:
            return {
                    "id": self.goal_id,
                    "title": self.title,
                }