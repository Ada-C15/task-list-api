from flask import current_app
from app import db
from dataclasses import dataclass
import datetime

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

    def to_dictionary(self):
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