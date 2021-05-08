from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    def goal_to_json_response(self):
        return {"goal": 
                        {"id": self.goal_id,
                        "title": self.title}}

# # GOAL ROUTES - MOVE TO ROUTES !!!
# @goal_bp.route("", methods = ["POST"], strict_slashes = False)
# def create_goal():
#     try:
#         request_body = request.get_json()
#         new_goal = Goal(title=request_body["title"])
        
#         db.session.add(new_goal) # "adds model to the db"
#         db.session.commit() # does the action above
#         return new_goal.goal_to_json_response(), 201
#     except KeyError:
#         return {"details": "Invalid data"}, 400
