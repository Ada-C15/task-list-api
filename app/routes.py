from flask import request, Blueprint, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
import os
import requests



tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


# @tasks_bp.route("", methods=["GET", "POST"])
# def handle_tasks():
#     if request.method == "GET":
#         sort_query = request.args.get("sort")
#         if sort_query == "desc":
#             tasks = Task.query.order_by((Task.title.desc()))
#         elif sort_query == "asc":
#             tasks = Task.query.order_by(Task.title)
#         else:
#             tasks = Task.query.all()

#         tasks_response = []
#         for task in tasks:
#             tasks_response.append(task.dict_response())
#         return jsonify(tasks_response)

#     elif request.method == "POST":
#         form_data = request.get_json()

#         if "title" not in form_data\
#             or "description" not in form_data\
#                 or "completed_at" not in form_data:
#             return({"details":"Invalid data"}, 400)

#         new_task = Task(title=form_data["title"],
#                     description=form_data["description"],
#                     completed_at=form_data["completed_at"])

#         db.session.add(new_task)
#         db.session.commit()

#         return make_response({"task":new_task.dict_response()}, 201)



# @tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
# def single_task(task_id):
#     task = Task.query.get(task_id)
#     if task is None:
#         return make_response("", 404)

#     if request.method == "GET":
#         return {"task":task.dict_response()}

#     elif request.method == "PUT":
#         form_data = request.get_json()

#         task.title = form_data['title']
#         task.description = form_data["description"]
#         task.completed_at = form_data["completed_at"]

        
#         db.session.commit()

#         return jsonify({"task":task.dict_response()}), 200

#     elif request.method == "DELETE":
#         db.session.delete(task)
#         db.session.commit()

#         return {"details":
#                 (f'Task {task.task_id} "{task.title}" successfully deleted')
#                 }

# @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_complete(task_id):
#     task = Task.query.get(task_id)

#     if task:
#         task.completed_at = datetime.utcnow()
#         path = "https://slack.com/api/chat.postMessage"
#         request_header = {
#                     "Authorization": os.environ.get("SLACK_TOKEN")
#                     }
#         data = {
#             "channel": "task-notifications",
#             "text": f"Someone just completed the task {task.title}."
#             }
#         requests.post(path, data=data, headers=request_header)
#         return({"task":task.dict_response()}, 200)
#     else: 
#         return make_response("", 404)

# @tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(task_id):
#     task = Task.query.get(task_id)

#     if task:
#         task.completed_at = None
#         db.session.commit()
#         return {"task":task.dict_response()}

#     else:
#         return make_response("", 404)

@goals_bp.route("", methods=["GET", "POST"])
def handle_goals():
    if request.method == "GET":
        goals = Goal.query.all()
        goals_response = []
        for goal in goals:
            goals_response.append(goal.goal_dict())

        return jsonify(goals_response),200

    elif request.method == "POST":
        form_data = request.get_json()

        if "title" not in form_data:
            return({"details":"Invalid data"}, 400)

        new_goal = Goal(title=form_data["title"])

        db.session.add(new_goal)
        db.session.commit()

        return make_response({"goal": new_goal.goal_dict()}, 201)


@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def single_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)

    if request.method == "GET":
        return({"goal": goal.goal_dict()}, 200)

    elif request.method == "PUT":
        form_data = request.get_json()

        goal.title = form_data['title']

        db.session.commit()

        return jsonify({"goal": goal.goal_dict()}), 200

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()

        return {"details":
                (f'Goal {goal.goal_id} "{goal.title}" successfully deleted')
                }, 200
