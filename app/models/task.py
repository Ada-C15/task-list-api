from flask import current_app
from app import db
from flask import Blueprint


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(50)) 
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)
    

    def create_json(self):
        if self.completed_at == None:
            completed = False
        else:
            completed = True

        return {
                'id' : self.id,
                'title' : self.title,
                'description' : self.description,
                'is_complete' : completed
        }

    def create_json_with_goal_id(self):
        if self.completed_at == None:
            completed = False
        else:
            completed = True

        return {
                'id' : self.id,
                'goal_id' : self.goal_id,
                'title' : self.title,
                'description' : self.description,
                'is_complete' : completed
        }
    
    def from_json(request_dict):
        new_task = Task(
        title = request_dict["title"],
        description = request_dict["description"],
        completed_at = request_dict["completed_at"]
        )

        return new_task