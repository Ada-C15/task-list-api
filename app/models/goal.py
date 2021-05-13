from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

#PARENT CLASS
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    #relating to tasks database
    tasks = db.relationship('Task', backref='goal', lazy=True)

            
