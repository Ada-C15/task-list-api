from flask import current_app
from app import db

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    __tablename__ = "goal"
    tasks = db.relationship('Task', backref='goal', lazy=True)  

    def api_response(self):
        return (
            {
                "id": self.id,
                "title": self.title,
                }
            ) 