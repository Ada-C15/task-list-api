from flask import current_app
from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    __tablename__= "goals"

    def to_dict(self):
        
        return {
            "id": self.id,
            "title": self.title
            }
