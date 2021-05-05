from flask import Blueprint, request, make_response, jsonify
from app import db 
from app.models.task import Task

tasks_bp = Blueprint(
    "tasks",
    __name__, 
    url_prefix="/tasks"
)


@tasks_bp.route("", methods=["POST"])
def add_new_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(new_task.to_json(), 201)