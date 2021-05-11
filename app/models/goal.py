from flask import current_app
from app import db

# this is the 1 in 1-to-many; task is the many
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    # youtube guy creates necessary psuedo-column; it doesnt affect anything on the db level 
    # simply a way for Flask-SQLAlchemy to associate one model w another

    # added a property called tasks
    #  By using a backref, each task will have a property called goal, which refers to entire goal object to which task belongs
    tasks = db.relationship('Task', backref='task', lazy=True) # (model we're asso'ing w Goal, -, -) ;;; USED TO BE backref='tasks'

    # we can now find a specific goal and get all of the tasks asso'd w it with 
        # goal.tasks ('tasks' as in var name, not backref)
    # find specific task with
        # task.goal (backref-value.goal-instance)


    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title,
            #"tasks": self.tasks # >>> this fails 4 tests in wave 5 
            }