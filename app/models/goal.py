from flask import current_app
from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # tasks = db.relationship("Task", backref="goal")
    __tablename__ = "goals"

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            #"tasks": self.tasks
        }
    
    def to_string(self):
        return f"{self.id}: {self.title} Description: {self.description}"