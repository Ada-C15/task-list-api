from app import db
from flask import Blueprint, request, jsonify
from app.models.task import Task
from sqlalchemy import asc, desc
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()

    if ("title" not in request_body.keys() or
        "description" not in request_body.keys() or
        "completed_at" not in request_body.keys()):
        return {"details": "Invalid data"}, 400
    
    new_task = Task(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = request_body["completed_at"])
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_json()
    }, 201


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    title_from_url = request.args.get("title")

    if title_from_url:
        tasks = Task.query.filter_by(title = title_from_url)
    elif request.args.get("sort") is not None:
        sort = request.args.get("sort")
        if sort == "asc":
            tasks = Task.query.order_by(asc(Task.title))
        elif sort == "desc":
            tasks = Task.query.order_by(desc(Task.title))

    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response), 200


def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False


@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes = False)
def get_task_by_id(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return ("", 404)

    if not is_int(task_id):
        return ("", 404)

    return {"task": task.to_json()}, 200


@tasks_bp.route("/<task_id>", methods = ["PUT"], strict_slashes = False)
def update_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return ("", 404)

    form_data = request.get_json()

    task.title = form_data["title"]
    task.description = form_data["description"]
    task.completed_at = form_data["completed_at"]

    db.session.commit()

    return {"task": task.to_json()}, 200


@tasks_bp.route("/<task_id>", methods = ["DELETE"], strict_slashes = False)
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return ("", 404)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}, 200


@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"], strict_slashes = False)
def mark_task_complete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return ("", 404)

    task.completed_at = datetime.now()

    db.session.commit()

    return {"task": task.to_json()}, 200

@tasks_bp.route("/<task_id>/make_incomplete", methods = ["PATCH"], strict_slashes = False)
def mark_task_incomplete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return ("", 404)