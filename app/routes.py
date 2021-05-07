from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title)
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete()
            })
        return jsonify(tasks_response)

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body\
            or "completed_at" not in request_body:
            return ({
                "details": "Invalid data"
            }, 400)
        else:
            new_task = Task(title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"])

            db.session.add(new_task)
            db.session.commit()

            return ({
                "task": {
                    "id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": new_task.is_complete()
            }}, 201)

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        if task.goal_id:
            return {
                "task": {
                    "id": task.task_id,
                    "goal_id": task.goal_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": task.is_complete()
            }}
        else:
            return {
                "task": {
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": task.is_complete()
            }}
    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        return {
                "task": {
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": task.is_complete()
            }}
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return {
            "details": (f'Task {task.task_id} "{task.title}" successfully deleted')
        }

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    task.completed_at = datetime.utcnow()

    db.session.commit() # Do I need this for PATCH?

    client = WebClient(token=os.environ.get("SLACK_KEY"))

    channel_id = "C021GPYFGKT"

    client.chat_postMessage(
        channel=channel_id,
        text=(f"Someone just completed the task {task.title}")
    )

    # python requests HTTP package
    #requests.get('https://slack.com/api/chat.postMessage', auth={"Authorization": os.environ.get("SLACK_KEY")})

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True # is this better if it uses is_complete()?
        }
    }

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    task.completed_at = None

    db.session.commit() # Do I need this for PATCH?

    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False # is this better if it uses is_complete()?
        }
    })

@goals_bp.route("", methods=["POST", "GET"])
def handle_goals():

    if request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body:
            return ({
            "details": "Invalid data"
            }, 400)

        new_goal = Goal(
            title=request_body["title"])

        db.session.add(new_goal)
        db.session.commit()

        return ({
            "goal": {
                "id": new_goal.goal_id,
                "title": new_goal.title
            }
        }, 201)
    elif request.method == "GET":
        goals = Goal.query.all()

        goals_response = []
        for goal in goals:
            goals_response.append({
                "id": goal.goal_id,
                "title": goal.title,
            })
        return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)

    if request.method == "GET":
        return {
            "goal": {
                "id": goal.goal_id,
                "title": goal.title
        }}
    elif request.method == "PUT":
        form_data = request.get_json()

        goal.title = form_data["title"]

        db.session.commit()

        return {
                "goal": {
                    "id": goal.goal_id,
                    "title": goal.title
            }}
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return {
            "details": (f'Goal {goal.goal_id} "{goal.title}" successfully deleted')
        }

@goals_bp.route("/<goal_id>/tasks", methods=["GET", "POST"])
def handle_goals_tasks(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)

    if request.method == "GET":
        tasks = Task.query.filter_by(goal_id=goal.goal_id)

        tasks_response = []
        for task in tasks:
            tasks_dict = {
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete()
            }
            tasks_response.append(tasks_dict)

        return {
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": tasks_response
        }

    elif request.method == "POST":
        request_body = request.get_json()

        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal.goal_id

        db.session.commit()

        return {
            "id": goal.goal_id,
            "task_ids": request_body["task_ids"]
        }
