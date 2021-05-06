from flask import Blueprint
from app import db
from flask import request
from .models.task import Task
# from .models.goal import Goal
from flask import jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def tasks_index():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def single_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None), 404
    return jsonify({"task":task.to_json()}), 200

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return jsonify({"details":"Invalid data"}), 400
    
    new_task = Task(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = request_body["completed_at"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task":new_task.to_json()}), 201
    

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None), 404
    
    form_data = request.get_json()
    task.title = form_data["title"]
    task.description = form_data["description"]
    task.completed_at = form_data["completed_at"]
    db.session.commit()
    return jsonify({"task":task.to_json()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"details":f'Task {task.id} "{task.title}" successfully deleted'}), 200