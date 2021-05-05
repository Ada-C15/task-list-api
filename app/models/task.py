from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    #confirm extra steps to make this accept null
    #how can i set to none?
    completed_at = db.Column(db.DateTime)
