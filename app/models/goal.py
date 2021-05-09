from flask import current_app
from app import db
from dataclasses import dataclass
import datetime

@dataclass
class Goal(db.Model):
    id: int
    title: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # description = db.Column(db.String)
    # completed_at = db.Column(db.DateTime, nullable = True) 

    def to_dictionary(self):
        return {
            "id": self.id,
            "title": self.title
            # "description": self.description,
            # "is_complete": self.completed_at != None
            }