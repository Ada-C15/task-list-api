from app import db
from datetime import datetime
from flask import current_app
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    # relating to goal id by assigning new variable name for "id"
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),nullable=True)
    

    # helper function to convert "complete" to true or false
    def complete_helper(self):
        if self.completed_at == None: # if empty return false, if not empty return true
            complete = False
        else:
            complete = True
        return complete
    

    def display_tasks(self):
        if self.goal_id:
            return {
                "id": self.id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.complete_helper()
                }        
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.complete_helper()
            }

