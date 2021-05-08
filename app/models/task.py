from flask import current_app
from app import db
import datetime
# python > json > sql
class Task(db.Model): # model is a table w the following columns
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # define how model attrs map to databases
    title = db.Column(db.String)                                            # migrations do the mapping work
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

# customized 'to_json' method - made all tests pass
    def to_json(self):
        if self.completed_at:
            check_completion = True
        else:
            check_completion = False
        
        return { # way of serializing the data to pass it back and forth
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": check_completion
        }
