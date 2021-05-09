from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False) #add nullable=False ?? what is this?
    # Establishing one to many relationships to Task Model by adding
    # tasks ==>  like person to dogs
    tasks = db.relationship('Task', backref="goal", lazy=True)
    
    def goal_to_json_response(self):
        return {"goal": 
                        {"id": self.goal_id,
                        "title": self.title}}

    def simple_response(self):
        return {"id": self.goal_id,
                "title": self.title}

    def one_goal_tasks_response(self, goal_id):
        return {"id": self.goal_id,
                "title": self.title,
                "tasks": 
                    [{ "id": tasks.id,
                        "goal_id": self.goal_id,
                        "title": tasks.title,
                        "description": tasks.description,
                        "is_complete": bool(tasks.completed_at)}]}

# @goal_bp.route("/<goal_id>/tasks", methods = ["GET"])
# def post_task_ids_to_goal(goal_id):
    
#         # request_body = request.get_json()   # should be a dictionary like:
#         #                                     # {"task_ids": [1, 2, 3]}
#         goal = Goal.query.get(goal_id)  # the instance of thi goal id including the task ids
#         # store list of tasks given in the request body (task_ids)
#         task_ids = request_body["task_ids"]  # task_ids - should be a list [1,3,4]
        
#         if goal and task_ids: 
#         for task_id in task_ids:
#             task = Task.query.get(task_id) # I WANT TASKS WITH THOSE ID S IN TASK IDS 
#             # append those tasks that you queried into goal with given id
#             goal.tasks.append(task) # this is a field 
#             db.session.commit()
#         # display this info into response as json 
#         return {"id": int(goal_id), "task_ids": task_ids},200

#     try:    
#     except:
#         # return make_response(""), 404 ## not found
#         return {"details": "Invalid data"}, 400