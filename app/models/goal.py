from flask import current_app
from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy=True)

    def create_response(self):
        return{
            "id": self.goal_id,
            "title": self.title,
        }
    
    def return_tasks(self):
        return {
            "id": self.goal_id,
            "task_ids": self.tasks
        }
    def return_goal_tasks(self):
        return{
            "id": self.goal_id,
            "title": self.title,
            "tasks": self.tasks
        }