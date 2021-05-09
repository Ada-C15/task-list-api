from flask import current_app
from app import db
from flask import request, Blueprint, make_response, jsonify

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    # def is_complete_helper_function(self):
    #     if Task.completed_at is None:
    #         is_complete == False
    #         return is_complete
    #     else:
    #         is_complete == True
    #         return is_complete

    