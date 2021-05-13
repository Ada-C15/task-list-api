from flask import current_app
from flask.helpers import get_template_attribute
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    # a task with a null value for completed_at has NOT been completed:
    completed_at = db.Column(db.DateTime, nullable=True)
    # ForeignKey refers to the Goal Model Primary Key in the table "goals" and column "id"
    goals_id = db.Column(db.Integer, db.ForeignKey("goals.id"), nullable=True)  

    __tablename__= "tasks"

    def to_dict(self):

        make_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None
        }
        if self.goals_id:
            make_dict["goal_id"] = self.goals_id
            
        return make_dict