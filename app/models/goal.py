from flask import current_app
from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def create_goal_json(self):

        return {
                'id' : self.id,
                'title' : self.title
                #'tasks' : self.tasks
        }
