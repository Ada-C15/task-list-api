from flask import current_app
from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(100))
    completed_at = db.Column(db.DateTime, nullable=True)
    # minute 25:00 at https://www.youtube.com/watch?v=81UwMhpuxJk&ab_channel=RithmSchoolRithmSchool 
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True) # foreign key(name-of-table.that-table's-column)

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