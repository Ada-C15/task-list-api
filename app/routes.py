from flask import Blueprint
from app import db
from .models.task import Task
from flask import request, jsonify, make_response
from datetime import datetime

task_list_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_list_bp.route("", methods = ["POST"], strict_slashes = False)
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response(jsonify({"details": f"Invalid data" }), 400)
    
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])
    
    db.session.add(new_task)
    db.session.commit()

    return make_response({
        "task": new_task.to_json()}, 201)

@task_list_bp.route("", methods = ["GET"])
def get_all_tasks():
    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(Task.title)
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
        
    task_list = []
    for task in tasks:
        task_list.append(task.to_json())
    return make_response(jsonify(task_list))

@task_list_bp.route("/<task_id>", methods = ["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response(" ", 404)

    if request.method == "GET":
        return make_response(jsonify({
            "task": task.to_json()
        }))

    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()
        return make_response(jsonify({"task": task.to_json()}))

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({
            "details": f'Task {task.task_id} "{task.title}" successfully deleted'})