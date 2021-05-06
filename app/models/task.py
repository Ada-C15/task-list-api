from flask import current_app
from app import db
import datetime
# this is telling flask about my database task table


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    def completed_at_helper(self):
        if self.completed_at == None:
            complete = False
        else:
            complete = True
        return complete

    def json_object(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at_helper()
        }
    # Use this helper function any time the return is expected to be complete
