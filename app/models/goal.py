from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    # tasks = db.relationship('Task', backref='task', lazy=True)

    def goal_to_json_format(self):
        return {
            "id": self.goal_id,
            "title": self.title,
            }
    
    # def add_task_response_to_json(self):

    #     return {
    #         "id": self.goal_id,
    #         "task_ids": [t.task_id for t in self.tasks]
    #     }

    # def tasks_to_many_goals_to_json_format(self):
    #     return {
    #         "id": self.goal_id,
    #         "title": self.title,
    #         "tasks": [t.to_json_format() for t in self.tasks]
    #     }

