from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title =  db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))

    def convert_complete(self):
        if self.completed_at == None:
            complete = False
        else:
            complete = True
        return complete

    def to_json(self):
        if self.goal_id:
            return{
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.convert_complete()
            }
        return{
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.convert_complete()
            }