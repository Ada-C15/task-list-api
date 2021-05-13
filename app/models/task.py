from flask import current_app
from app import db
from app.models.goal import Goal

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    __tablename__ = "task"
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True) 

    def completed(self):
        return bool(self.completed_at)       
    
    def api_response(self, complete=False):
        response_body = {
                        "id": self.id,
                        "title": self.title,
                        "description": self.description,
                        "is_complete": self.completed()
                        }
        if complete:  
            response_body["is_complete"]= self.completed() 
        
        if self.goal_id:
            response_body["goal_id"] = self.goal_id
        return response_body
