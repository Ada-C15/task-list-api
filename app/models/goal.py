from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    
    def to_json_goal(self):
        
        return {
                "goal":     
                       {
                            "id": self.goal_id,
                            "title": self.title,
                        }
                     }
    def to_json_goal_no_key(self):    
                return {
                            "id": self.goal_id,
                            "title": self.title
                        }