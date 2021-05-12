from flask import current_app
from app import db


class Goal(db.Model): # Goal is the parent class
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)
    

    def to_json(self):

        return {
            "id": self.goal_id,
            "title": self.title
        }

    def to_json_three(self):

        task_list = []
        for task in self.tasks:
            if task.completed_at:
                complete = True
            else:
                complete = False
        
            task_list.append({
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": complete
            })

        return {
            "id": self.goal_id,
            "title": self.title,
            "tasks": task_list
        }