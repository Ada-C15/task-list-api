from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def get_resp(self):
        return{
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": (False if self.completed_at == None else True )
            }
        # if self.completed_at == None:
        #     return {
        #         "id": self.task_id,
        #         "title": self.title,
        #         "description": self.description,
        #         "is_complete": False
        #     }

        # else:
        #     return {
        #         "id": self.task_id,
        #         "title": self.title,
        #         "description": self.description,
        #         "is_complete": True
        #     }
