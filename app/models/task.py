from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(100))
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True) # prettyprinted on youtube explains concept: https://www.youtube.com/watch?v=juPQ04_twtA&t=412s&ab_channel=PrettyPrinted 

    def to_json(self):
        if self.completed_at:
            check_completion = True
        else:
            check_completion = False

        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": check_completion
            }