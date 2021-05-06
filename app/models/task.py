from app import db
from flask import current_app


class Task(db.Model):

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True) #autoincrement optional
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True) #nullable value

#add jsonify class method