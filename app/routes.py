from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from app import db
from datetime import datetime
#import requests
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
# from task-list-api.env import SLACK_KEY

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
