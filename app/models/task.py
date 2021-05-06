from flask import current_app
from app import db



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    
    #how to make it nullable and change once task is complete? 
    #what's the difference between False & None in this case in the tests?
    completed_at = db.Column(db.DateTime, nullable = True)
   # is_complete = db.Column()

    def some_function(task):
        if request_body["completed_at"] == None: #is this null??
            task.completed_at = False
            return task.completed_at

    #     if is_complete = True

    #     else is_complete = False

