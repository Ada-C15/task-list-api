from flask import current_app
from app import db


class Task(db.Model):
    """
    Attributes:
        task_id
        title   
        description 
        completed_at
        goal_id
    """
    task_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)


    
    def to_python_dict(self):
        """
            Input:  An instance of Task 
            Output: The instance of Task in a python dictionary, is_complete attribute is assigned
                    a boolean data type value
        """
        if self.completed_at == None:
            is_complete = False
        else:
            is_complete = True 
            
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
    
    
    def to_python_dict_goal_id(self):
        """
            Input:  An instance of Task 
            Output: Returns the Task instance in a python dictionary adding a "goal_id" key to the
                    dictionary 
        """
        result = self.to_python_dict()
        result["goal_id"] = self.goal_id
        return result 