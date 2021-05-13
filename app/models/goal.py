from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    


    # def display_goals(self):
    #     return { 
    #         "id": self.id,
    #         "title": self.title
    #         }
            
