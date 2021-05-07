from flask import current_app
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def check_if_complete(self):
        if self.completed_at == None:
            return False
        else:
            return True

    def to_json(self):

        return {
            "task": {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.check_if_complete() # self.completed at != None
                }
        }



# return jsonify({
#     "task": {
#         "id": new_task.task_id,
#         "title": new_task.title,
#         "description": new_task.description,
#         "is_complete": False
#         }
# }), 201



