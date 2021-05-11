from flask import current_app
from app import db

# not migrating to my database, first i was missing the title and 
# then i deleted the table ugh  
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable = True)


    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }   


