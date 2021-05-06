from app import db
from app.models.task import Task
from flask import Blueprint, make_response, request, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def handle_tasks():

    request_body = request.get_json()

    new_task = Task(title=request_body['title'],
                    description=request_body['description'],
                    completed_at=request_body['completed_at'])

    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }

    return make_response(jsonify(response), 201)