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
    
#helper function-returns goal attributes in corrected format
    def goal_to_json(self):
        goal_dict={"id": self.goal_id,
            "title": self.title}
        return goal_dict

