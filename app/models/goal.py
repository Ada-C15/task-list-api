from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models.task import Task # is this necessary?


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)
