from flask import request, Blueprint, make_response
from app import db
from flask import jsonify
from .models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["POST"], strict_slashes=False)
def add_task():
    request_body = request.get_json()
    print(request_body)
    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return jsonify({
        "details": "Invalid data"
        }), 400
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
            "task":{
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.convert_complete()
    }}), 201

@task_bp.route("", methods=["GET"], strict_slashes=False)
def task_index():
    tasks = Task.query.all()
    task_response = []
    for task in tasks:
        task_response.append(task.to_json())
    return jsonify(task_response), 200

@task_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_task(task_id):
    task = Task.query.get(task_id)
    if task: 
        return jsonify({
            "task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.convert_complete()
            }
            }), 200
    return "", 404

@task_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return jsonify({
            "task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.convert_complete()
            }
            }), 200
    return "", 404

@task_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({
            "details": (f'Task {task.task_id} "{task.title}" successfully deleted')
        }), 200
    return "", 404