from flask import current_app
from app import db
from dataclasses import dataclass
import datetime

@dataclass
class Task(db.Model): ### WAVE 1 ###
    id: int
    title: str
    description: str
    completed_at: datetime # turn this into a boolean?
# you need these four lines in because they provide the necessary format that jsonify can work with???
# there is some kind of magic going on in the background.

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True) # what is the data type for date?

    # __tablename__ = "task" # need =ed to remove the __tablename__ it was preventing the jsonify()? there was an error about it    

    def to_dictionary(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None
            }
    # this to_dictionary(self) method will format each task instance as a dictionary that can be wrapped/converted in JSON format with the function jsonify()