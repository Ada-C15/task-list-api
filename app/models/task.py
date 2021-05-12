from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)

    def serialize(self):
        result = {
            'id': self.task_id,
            'title': self.title,
            'description': self.description,
            'is_complete': self.completed_at != None
        } 
        return result     

  
    

