from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET"])
def handle_tasks_get():
    """
    Get Tasks: Getting Saved Tasks
    """
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        })
    return jsonify(tasks_response)


@tasks_bp.route("", methods=["POST"])
def handle_tasks_post():
    """
    Create a Task: Valid Task With null completed_at
    """
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"]
                    )

    db.session.add(new_task)
    db.session.commit()

    retrieve_task = Task.query.get(1)

    return {
        "task": {
            "id": retrieve_task.task_id,
            "title": retrieve_task.title,
            "description": retrieve_task.description,
            "is_complete": retrieve_task.is_complete
        }
    }, 201


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_one_task_get(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response(404)

    if task:
        return ({
            "task": {
                "task_id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete
            }
        }, 200)
