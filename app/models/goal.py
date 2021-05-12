from flask import current_app
from app import db

class Goal(db.Model):
    __tablename__ = 'goal'
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # Establishes parent relationship with Task/s
    tasks = db.relationship("Task", lazy=True, backref="goal")
    
    def goal_data_structure(self):
        goal_data_structure = {
                    "goal":{
                    "id":self.goal_id,
                    "title":self.title
                }}

        return goal_data_structure

    # creates a goal dictionay with info on all tasks in goal
    def tasks_data_structure(self):
        tasks = []
        for task in self.tasks:
            # calls on task method to populate data
            tasks.append(task.task_data_structure()['task'])

        tasks_data_structure = {
                    "id":self.goal_id,
                    "title":self.title,
                    "tasks": tasks
                }
        return tasks_data_structure