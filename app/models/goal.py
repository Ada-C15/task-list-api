from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    #helper function to return in json format
    def goal_to_json(self):
        return {
        "id": self.goal_id,
        "title": self.title,
        }