from flask import Blueprint
from app import db 
from app.models.task import Task 
from flask import request, Blueprint, make_response 
from flask import jsonify


task_list_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_list_bp.route("/tasks", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title = request_body["title"], description = request_body["description"], complete_at = request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Task {new_task.title} successfully created", 201)