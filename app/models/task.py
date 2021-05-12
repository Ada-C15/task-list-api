from flask import current_app
from app import db
from app.models.goal import Goal


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) #autoincrement=True
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    __tablename__ = "task"
    #'goal' is looking at goal bd and not python Goal class. 
    #this creates a real (not pseudo column)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True) 

    # def completed(self):
    #     is_complete = False
    #     if self.completed_at is True:
    #         is_complete = True
    #     return is_complete    

    def completed(self):
        return bool(self.completed_at)       
    
    def api_response(self, complete=False):
        if complete == True:
            return (
            {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": True
                }
            ) 
        else:
            return (
                {
                    "id": self.id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": self.completed()
                    }
                ) 