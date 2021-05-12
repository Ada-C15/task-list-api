from app import db
from app.models.task import Task
from datetime import datetime
from flask import request, Blueprint, make_response, jsonify
import requests
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.models.goal import Goal
goals_bp = Blueprint(
    "goals", __name__, url_prefix="/goals")

tasks_bp = Blueprint(
    "tasks", __name__, url_prefix="/tasks")


# -------------------------
# WAVE 1 - TASK ENDPOINTS
# -------------------------
@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()

    if "title" in request_body and "description" in request_body and "completed_at" in request_body:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"]
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"task": new_task.to_dict()}), 201
    else:
        return make_response({"details": "Invalid data"}, 400)


# WAVE 2
@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def task_index():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return make_response(jsonify(tasks_response), 200)


# WAVE 1
@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        return jsonify({"task": task.to_dict()}), 200

    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data['description']
        task.completed_at = form_data["completed_at"]
        db.session.commit()

        return jsonify({"task": task.to_dict()}), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        task_response = {
            "details": f'Task {task.task_id} "{task.title}" successfully deleted'}
        return make_response(task_response), 200


# WAVE 3
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def handle_incomplete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    else:
        task.completed_at = None
        db.session.commit()
        return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def handle_complete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    else:
        task.completed_at = datetime.now()
        db.session.commit()
        call_slack_api(task)
    return jsonify({"task": task.to_dict()}), 200


# WAVE 4
def call_slack_api(task):
    SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    url = "https://slack.com/api/chat.postMessage"
    payload = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"}
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
    }
    return requests.request("POST", url, headers=headers, data=payload)


# def call_slack_api(task):
#     client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
#     channel_id = "T0226NANZ9N"
#     try:
#         result = client.chat_postMessage(
#             channel=channel_id,
#             text=f"Someone just completed the task {task.title}"
#         )
#         logger.info(result)

#     except SlackApiError as e:
#         logger.error(f"Error posting message: {e}")


# -------------------------
# WAVE 5 - GOAL ENDPOINTS
# -------------------------

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():
    request_body = request.get_json()
    if "title" in request_body:
        new_goal = Goal(
            title=request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({"goal": new_goal.to_dict()}), 201
    return make_response({"details": "Invalid data"}, 400)


@goals_bp.route("", methods=["GET"], strict_slashes=False)
def goal_index():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return make_response(jsonify(goals_response), 200)


@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)

    if request.method == "GET":
        return jsonify({"goal": goal.to_dict()}), 200

    elif request.method == "PUT":
        form_data = request.get_json()
        goal.title = form_data["title"]
        db.session.commit()
        return jsonify({"goal": goal.to_dict()}), 200

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        goal_response = {
            "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}
        return make_response(goal_response), 200
