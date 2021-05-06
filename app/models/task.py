from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime) 
    
    # created a helper function to conver completed_at to is_complete.
    def convert_complete(self):
        if self.completed_at == None:
            complete = False
        else:
            complete = True

        return complete

    # def to_json(self):
    #     return {
    #         “id”: self.task_id,
    #         “title”: self.title,
    #         “description”: self.description,
    #         “is_complete”: self.completed_at !=None
    #     }