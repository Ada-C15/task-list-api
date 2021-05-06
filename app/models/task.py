from flask import current_app
from app import db
#from sqlalchemy.types import DateTime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title= db.Column(db.String)
    description= db.Column(db.String)
    completed_at=db.Column(db.DateTime, nullable=True, default=None)

#runs when there is a task completed
    def is_complete(self):
        if self.completed_at==None:
            return False
        else:
            return True