from flask import current_app
from app import db
from datetime import datetime


class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)


    def update_completed(self):
        self.completed_at = datetime.now()
    
    def task_data_structure(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False
            
        task_data_structure = {
                    "task":{
                    "id":self.task_id,
                    "title":self.title,
                    "description":self.description,
                    "is_complete": is_complete
                }}

        return task_data_structure