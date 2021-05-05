from app import db
from app.models.task import Task
from flask import request, Blueprint, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def handle_tasks():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                description=request_body["description"], 
                completed_at=request_body["is_complete"])

    db.session.add(new_task)
    db.session.commit()

    return make_response("201 CREATED", 201)


# @tasks_bp.route("/<task_id>", methods=["GET, "PUT", "DEL])

