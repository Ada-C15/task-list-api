# from flask import current_app
from app import db
from dataclasses import dataclass
import datetime
# from .models.goal import Goal

@dataclass # do i need this decorator and what is it doing?
class Task(db.Model): 
    id: int
    title: str
    description: str
    completed_at: datetime

# you need these four lines in because they provide the necessary format that jsonify can work with???
# there is some kind of magic going on in the background?

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True) 
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    # goal = db.relationship('Goal', backref='task')
    # goal = db.relationship('Goal', back_populates='task')

    def to_dictionary(self):
        if self.goal_id:
            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "goal_id": self.goal_id,
                "is_complete": self.completed_at != None
                }
        else:
            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at != None
                }

    # this to_dictionary(self) method will format each task instance as a dictionary that, 
    # with the function jsonify(), can be wrapped/converted in JSON format 
    # this is the refactor that Chris did in the 3rd video of Create and Read. 
    # I named the method "to_dictionary" so it's easier to tell apart from get_json() 
    # which is a different function that comes in the pytest package