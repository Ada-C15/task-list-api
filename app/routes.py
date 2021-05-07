from app import db
from flask import Blueprint, request, jsonify
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
#Creates a task object using provided request body information
def create_task():
    request_body = request.get_json()
    new_task = Task(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = request_body["completed_at"])
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_json()
    }, 201

#Returns a list of all the tasks in the database
@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    title_from_url = request.args.get("title")

    if title_from_url:
        tasks = Task.query.filter_by(title = title_from_url)
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

@tasks_bp.route("/<task_id>", methods = ["UPDATE"], strict_slashes = False)

