from flask import current_app
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
