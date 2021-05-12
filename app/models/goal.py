from flask import current_app
from app import db



class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", backref="goal", lazy=True)

    def is_complete(self):
        if self.completed_at is None:
            return False
        else:
            return True

    def to_dict(self):
        return {
            "id": self.goal_id, 
            "title": self.title
            }   

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }
