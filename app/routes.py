from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify
from sqlalchemy import asc, desc
from datetime import datetime
import requests
from app import slack_key

task_list_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Wave 1
# make a post request
# add conditionals and if invalid return code 400

@task_list_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    required_properties = ["title", "description", "completed_at"]
    for prop in required_properties:
        if prop not in request_body:
            return make_response({"details": "Invalid data"}), 400
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit() 
    
    # returning single task created by calling to_json on new task
    return make_response({"task": new_task.to_json()}), 201

@task_list_bp.route("", methods=["GET"])
def get_all_tasks():
    sort = request.args.get("sort")
    if sort == "asc":
        tasks = Task.query.order_by(asc("title"))
    elif sort == "desc":
        tasks = Task.query.order_by(desc("title"))
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        # building a list of jsons by calling to_json on each task
        tasks_response.append(task.to_json())

    return jsonify(tasks_response)


@task_list_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    elif request.method == "GET":
        return make_response({"task": task.to_json()}), 200
    
    elif request.method == "PUT":
        task_data = request.get_json()
        task.title = task_data["title"]
        task.description = task_data["description"]

        db.session.commit()

        return make_response({"task": task.to_json()}), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})


@task_list_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    # Consider using the keyword arguments data, json, and/or headers
    url = "https://slack.com/api/chat.postMessage"
    data = {
        "channel": "C021ACT6H0B",
        "text": (f"Someone just completed the task {task.title}")
    }
    headers = {
        "Authorization": f"Bearer {slack_key}"
    }

    r = requests.post(url, data=data, headers=headers)

    if task is None:
        return make_response("", 404)
    else:
        task.completed_at = datetime.utcnow()
        db.session.commit()

    return make_response({"task": task.to_json()})


@task_list_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    else:
        task.completed_at = None
        db.session.commit()

    return make_response({"task": task.to_json()})