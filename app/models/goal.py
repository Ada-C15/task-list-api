from flask import current_app
from sqlalchemy.orm import relationship
from app import db
from app.models.task import Task
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String)
    #__tablename__='goal'
    #child_tasks=db.relationship("Task", backref='goal', lazy=True)

