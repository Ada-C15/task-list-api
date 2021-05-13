from flask import current_app
from app import db



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    assoc_goal = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def is_complete_func(self):
        if self.completed_at == None:
            return False
        else:
            return True

    def to_dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "is_complete":self.is_complete_func()
            }

    def to_dict_goal(self):
        return {
            "id":self.id,
            "goal_id": self.assoc_goal,
            "title":self.title,
            "description":self.description,
            "is_complete":self.is_complete_func()
            }