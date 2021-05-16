from flask import current_app
from app import db







class Goal(db.Model):
    __tablename__= "goals"
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    tasks = db.relationship("Task", lazy=True, backref="goal")

    def to_json(self):
        if len(self.tasks) == 0: 
            return {"id": self.goal_id, 
            "title": self.title }
        else:
            return {"id": self.goal_id, 
                    "title": self.title, 
                    "tasks": self.tasks}