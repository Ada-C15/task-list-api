from flask import current_app
from app import db
from app.models.goal import Goal 


class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at= db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.goal_id"), nullable = True)
    __tablename__ = "tasks"


    def resp_json(self):
        my_fav_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at 
            else False
        }
        if self.goal_id:
            my_fav_dict["goal_id"] = self.goal_id
        return my_fav_dict
