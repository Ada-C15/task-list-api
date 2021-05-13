from flask import current_app
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key = True, nullable=False)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    
    def to_json(self):
        task = {
            "id": self.task_id, 
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }      
        if self.goal_id:
            task["goal_id"] = self.goal_id 
        return task

    @classmethod
    def sort(cls, query_param_value):
        if query_param_value == "desc":
            return cls.query.order_by(cls.title.desc()).all()
        elif query_param_value == "asc":
            return cls.query.order_by(cls.title).all()
        elif query_param_value == "desc_id":
            return cls.query.order_by(cls.task_id.desc()).all()
        elif query_param_value == "asc_id":
            return cls.query.order_by(cls.task_id).all()
        return cls.query.all()
