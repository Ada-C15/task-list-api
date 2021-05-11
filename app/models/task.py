from flask import current_app, jsonify
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def is_complete(self):
        """
        Checks if task has completed_at value and is complete
        """
        if self.completed_at is None:
            is_complete = False
        else:
            is_complete = True
        return is_complete

    # def to_json(self):
    #     """
    #     Outputs formatted JSON dictionary of task attributes
    #     """
    #     if self.goal_id:
    #         return {
    #             "task": {
    #                 "id": self.task_id,
    #                 "goal_id": self.goal_id,
    #                 "title": self.title,
    #                 "description": self.description,
    #                 "is_complete": self.is_complete()
    #         }}
    #     else:
    #         return {
    #                 "task": {
    #                     "id": self.task_id,
    #                     "title": self.title,
    #                     "description": self.description,
    #                     "is_complete": self.is_complete()
    #             }}

    def to_json(self):
        """
        Outputs formatted JSON dictionary of task attributes
        """
        if self.goal_id:
            return {
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
            }
        else:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
                }

    def from_json(self, input_data):
        """
        Converts JSON input data into new instance of Task
        """
        return self(title=input_data["title"],
        description=input_data["description"],
        completed_at=input_data["completed_at"])
