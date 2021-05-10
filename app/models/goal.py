from flask import current_app
from app import db

# this is the 1 in 1-to-many; task is the many
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    # youtube guy creates necessary psuedo-column for this 'tasks' value
    # the following line throws off a bunch of w5 tests now... ()
    tasks = db.relationship('Task', backref='larger_goal', lazy=True) # 'Task' and not 'task' bc looking at the class in python code

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title,
            #"task_ids": self.tasks >>> this fails 4 tests in wave 5
            }