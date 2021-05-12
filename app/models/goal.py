from flask import current_app
from app import db
# from app.models.task import Task

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    __tablename__ = "goal"
    #"Task" is the child. backref is what links back to the child. ie, if we had a Person and an pet, we could say "owner" here. 
    #and that will give the Pet a virtual column of owner, so here our Task will get a virtual column of "goal"
    #'Task' is looking at class in Python code (hence capital letter)
    #'tasks' is a pseudo-column 
    tasks = db.relationship('Task', backref='goal', lazy=True)  #when you query for goal, goal is loaded first and THEN task -?

    def api_response(self):
        return (
            {
                "id": self.id,
                "title": self.title,
                }
            ) 