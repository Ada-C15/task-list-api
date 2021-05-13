from flask import current_app
from app import db
from datetime import datetime
# this is telling flask about my database task table

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    def completed_at_helper(self):
        if self.completed_at == None:
            complete = False
        else:
            complete = True
        return complete

    def json_object(self):
        
        new_reponse = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at_helper()
        }
        if self.goal_id is not None:
            new_reponse["goal_id"] = self.goal_id
        return new_reponse
    # Use this helper function any time the return is expected to be complete ^^^
    