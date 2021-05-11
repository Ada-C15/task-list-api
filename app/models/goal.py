from flask import current_app
from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    

  # helper function to convert "complete" to true or false
    def complete_helper(self):
        if self.completed_at == None: # if empty return false, if not empty return true
            complete = False
        else:
            complete = True
        return complete
    

    def display_goals(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.complete_helper()
            }
