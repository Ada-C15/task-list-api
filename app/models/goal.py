from flask import current_app
from app import db

#WAVE 5
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    def goal_to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title
            } 