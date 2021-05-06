from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # do i set it to autoincrement?
    name = db.Column(db.String)
    time = db.Column(db.DateTime)
    date = db.Column(db.Date) # need to make sure it rounds to two decimals
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)