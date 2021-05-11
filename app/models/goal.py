from flask import current_app
from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    # Establishing one-to-many relationships to Task Model
    tasks = db.relationship('Task', backref="goal", lazy=True)
    
    def goal_to_json_response(self):
        '''
        Converts a Goal's instance into JSON response
        Output: Returns a Python dictionary in the shape JSON response
        for only one goal.
        '''
        return {"goal": 
                        {"id": self.goal_id,
                        "title": self.title}}

    def simple_response(self):
        '''
        Converts a Goals's instance columns (atributes?) into JSON response including
        the foreign key goal id.
        Output: Returns a Python dictionary in the shape JSON response 
        for a goal.
        '''
        return {"id": self.goal_id,
                "title": self.title}


