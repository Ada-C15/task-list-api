from flask import current_app
from app import db
from app.models.task import Task 


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref='goal', lazy=True)

    def goals_to_json(self): 
        return {
            "id": self.goal_id,
            "title": self.title
        }

    def specific_goal_to_json(self): 
        return {
            "goal": self.goals_to_json()
        }  
    
    def goal_associated_tasks(self, task): 
        task_list = []
        
        if task != None:
            task_list.append(task.tasks_to_json())
            
        return {
            "id": self.goal_id,
            "title": self.title,
            "tasks": task_list
        }

