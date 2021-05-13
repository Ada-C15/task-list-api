from flask import current_app
from app.models.task import Task
from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', lazy = True,)

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }

    def sort(query_param_value):
        if query_param_value == "desc":
            return Goal.query.order_by(Goal.title.desc()).all()
        elif query_param_value == "asc":
            return Goal.query.order_by(Goal.title).all()
        elif query_param_value == "desc_id":
            return Goal.query.order_by(Goal.goal_id.desc()).all()
        elif query_param_value == "asc_id":
            return Goal.query.order_by(Goal.goal_id).all()
        return Goal.query.all()