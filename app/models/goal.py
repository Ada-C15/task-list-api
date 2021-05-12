from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String)
    
    def goal_response(self):
        goal_response = {
            "goal":{   
                "id": self.goal_id,
                "title": self.title
                }
            }
        return goal_response
    
    def goal_response_lean(self):
        goal_response_lean = {
                "id": self.goal_id,
                "title": self.title
                }
        return goal_response_lean