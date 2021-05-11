from flask import Blueprint
from app.models.goal import Goal
from app import db
from flask import request, Blueprint, make_response, Response, jsonify
from datetime import date
import requests
from secrets import slack_token

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["GET", "POST"])
def handle_tasks():  # NameError
    if request.method == "GET":

        goals = Goal.query.all()
        goals_response = []

        for goal in goals:
            goals_response.append({
                "id": goal.goal_id,
                "title": goal.title
            })
        return jsonify(goals_response)
     

    elif request.method == "POST":  # CRUD CREATE
        # check for request body title and description, plus ensure both are strings
        request_body = request.get_json()

        if "title" not in request_body:
            return {
                "goal": f"Invalid title"
            }, 400

        goal = Goal(
            title=request_body["title"]
        )

        db.session.add(goal)
        db.session.commit()

        return {
            "goal": {
                "id": goal.goal_id,
                "title": goal.title
            }
        }, 201



# # getting 1 task


# @goal_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
# def handle_task(task_id):
#     task = Task.query.get(task_id)

#     if task == None:
#         return make_response(f"Task {task_id} not found", 404)

#     if request.method == "GET":
#         if task.completed_at == None:
#             completed_at = False
#         else:
#             completed_at = True
#         return {
#             "task": {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": completed_at
#             }
#         }
#     elif request.method == "PUT":
#         form_data = request.get_json()

#         task.title = form_data["title"]
#         task.description = form_data["description"]
#         task.completed_at = form_data["completed_at"]

#         db.session.commit()

#         if task.completed_at == None:
#             completed_at = False
#         else:
#             completed_at = True
#         return {
#             "task": {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": completed_at
#             }
#         }

#     elif request.method == "DELETE":
#         db.session.delete(task)
#         db.session.commit()
#         if task.completed_at == None:
#             completed_at = False
#         else:
#             completed_at = True
#         return {
#             "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
#         }

# @task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_complete(task_id):
#     task = Task.query.get(task_id)

#     if task == None:
#         return "",404

#     task.completed_at = date.today()  # todays date

#     db.session.commit()

#     r = requests.post(f"https://slack.com/api/chat.postMessage?channel=task-notifications&text=Someone just completed the task {task.title}", headers={"Authorization":slack_token})

#     return {
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": True
#         }
#     }

# @task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(task_id):
#     task = Task.query.get(task_id)
    
#     if task == None:
#         return "",404

#     task.completed_at = None

#     db.session.commit()

#     return {
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": False
#         }
#     }

