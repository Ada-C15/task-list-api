from flask import current_app
from app import db
from datetime import datetime   ## vs. with import datetime -  would be
                                ## datetime.datetime in line 40
                                ## like from random import randint 
# if I want to do the from_jason method?, import this:
# from flask import request # maybe I don't need it if I add arg to method

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    title = db.Column(db.String) # name of task or title of task
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    # adding one to many relationship  tasks to goal ==> dog to person 
    # nullable = task might not belong to a goal
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True) 

    def to_json_response(self):
        '''
        Converts a Task instance into JSON
        Output: Returns a Python dictionary in the shape of JSON response 
        that the API returns in the route that is called (GET).
        '''
        return {"task": 
                        {"id": self.id,
                        "title": self.title,
                        "description": self.description,
                        "is_complete": bool(self.completed_at)}
                }
                
    def task_to_json_response(self):
        '''
        Converts a Task's instance into JSON response
        Output: Returns a Python dictionary in the shape JSON response
        for only one task.
        '''
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)}

    def task_to_json_response_w_goal(self):
        '''
        Converts a Task's instance columns (atributes?) into JSON response including
        the foreign key goal id.
        Output: Returns a Python dictionary in the shape JSON response
        for a task that is part of a goal.
        '''
        return {"id": self.id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)}

    def set_completion(self):   
        '''
        Updates the attribute completed_at of the instance of a Task
        to the current date/time.
        '''
        complete_time = (datetime.now()).strftime("%c")
        self.completed_at = complete_time 

# TO DO WITH 
# Create a class method in Task named from_json()
# Converts JSON into a new instance of Task
# Takes in a dictionary in the shape of the JSON our API receives 
# in the create and update routes
# Returns an instance of Task

    @staticmethod
    def from_json_to_task(request_body):
        '''
        Converts JSON into a new instance of Task
        input: Takes in a dictionary in the shape of the JSON the API 
        receives 
        '''
        new_task = Task(title=request_body["title"],
                description=request_body["description"],
                completed_at = request_body["completed_at"])
        return new_task

