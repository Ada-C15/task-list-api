from app import db
from flask import Blueprint, request, jsonify
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
#Creates a task object using provided request body information
def tasks():
    request_body = request.get_json()
    new_task = Task(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = request_body["completed_at"])
    db.session.add(new_task)
    db.session.commit()

    completed_at_view = False
    if (new_task.completed_at is not None):
        completed_at_view = True

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": completed_at_view
        }
    }, 201

