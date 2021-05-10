# from flask import current_app
from app import db
from dataclasses import dataclass
# import datetime
# from .models.task import Task

@dataclass
class Goal(db.Model):
    id: int
    title: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)
    # i dont know exactly what backref does - like a virtual comlumn?
    # lazy means that when the relationship is established, 
    # ^^ it wont evaluate the task -- is this similar to an optional atribute of a class?

    # tasks = db.relationship('Task', back_populates="goal", lazy=True)
    # tasks = db.relationship('Task', uselist=True, backref='goal')

    def to_dictionary(self):
        return {
            "id": self.id,
            "title": self.title
            }
            