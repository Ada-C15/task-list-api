from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) #autoincrement=True
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    # is_complete = False

    # if completed_at is True:
    #     is_complete = True

    def completed(self):
        is_complete = False
        if self.completed_at is True:
            is_complete = True
        return is_complete    
    
    def api_response(self):
        return (
            {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed()
                }
            )
            # {"task": {
            #     "id": self.id,
            #     "title": self.title,
            #     "description": self.description,
            #     "is_complete": self.completed()
            #     }
            # })            